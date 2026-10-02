import os
import json
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# Configuration
# --------------------------------------------------

MODEL = "openai/gpt-4o-mini"
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not set. "
        "Please set it as an environment variable before running the app."
    )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)


# --------------------------------------------------
# Small LC knowledge base for the demo
# --------------------------------------------------

DOCUMENTS = [
    (
        "LC-2026-0091",
        "Letter of Credit LC-2026-0091. "
        "Beneficiary: Alpine Textiles Ltd. "
        "Goods: navy blue fabric, 220 gsm. "
        "Amount: USD 48,500. "
        "Tolerance: plus or minus 5 percent on amount and quantity."
    ),
    (
        "LC-2026-0114",
        "LC-2026-0114 explicitly prohibits transshipment. "
        "A presented bill of lading showed one transshipment at Hong Kong. "
        "The issuing bank treated this as a discrepancy and refused the presentation."
    ),
    (
        "LC-2026-0158",
        "LC-2026-0158 states approximately 60 metric tons with a 10 percent tolerance. "
        "Therefore quantities from 54 to 66 metric tons are acceptable. "
        "Documents must be presented within 21 days after shipment. "
        "The credit expires on 10 October 2026."
    ),
    (
        "Examiner rule",
        "A missing mandatory certificate is treated as a discrepancy "
        "even when the shipment is otherwise compliant."
    ),
]


# --------------------------------------------------
# Retrieval
# --------------------------------------------------

embedder = SentenceTransformer("all-MiniLM-L6-v2")

doc_texts = [text for _, text in DOCUMENTS]
doc_embeddings = embedder.encode(doc_texts)


def retrieve(query, k=2):
    query_embedding = embedder.encode([query])
    scores = cosine_similarity(query_embedding, doc_embeddings)[0]

    ranked = scores.argsort()[::-1][:k]

    return [
        {
            "name": DOCUMENTS[i][0],
            "text": DOCUMENTS[i][1],
            "score": float(scores[i]),
        }
        for i in ranked
    ]


# --------------------------------------------------
# Foundation-model helper
# --------------------------------------------------

def generate(system, user, max_tokens=300):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0,
    )

    return response.choices[0].message.content.strip()


# --------------------------------------------------
# Stage 1: Compliance classification
# --------------------------------------------------

CLASSIFICATION_PROMPT = """
You classify Letter of Credit document examination cases.

Return exactly one word:

compliant
or
discrepant

Do not include any explanation.
"""


def classify_case(note):
    return generate(
        CLASSIFICATION_PROMPT,
        f"Examiner note:\n{note}",
        max_tokens=10,
    ).lower()


# --------------------------------------------------
# Stage 2: Grounded retrieval answer
# --------------------------------------------------

GROUNDING_PROMPT = """
Answer using ONLY the supplied LC evidence.

If the evidence does not contain the answer, reply exactly:
The notes do not say.

Do not invent facts.
"""


def grounded_answer(question):
    hits = retrieve(question, k=2)

    context = "\n\n".join(
        f"[{h['name']}]\n{h['text']}"
        for h in hits
    )

    answer = generate(
        GROUNDING_PROMPT,
        f"EVIDENCE:\n{context}\n\nQUESTION:\n{question}",
    )

    return answer, hits


# --------------------------------------------------
# Stage 3: Structured discrepancy extraction
# --------------------------------------------------

STRUCTURED_PROMPT = """
Convert the examiner note into JSON.

Return exactly these fields:

{
  "lc_reference": "",
  "document_type": "",
  "discrepancy_category": "",
  "severity": "",
  "recommended_action": ""
}

If no valid discrepancy is described, use:

"discrepancy_category": "none"
"recommended_action": "accept"

Return valid JSON only.
"""


def extract_discrepancy(note):
    raw = generate(
        STRUCTURED_PROMPT,
        f"Examiner note:\n{note}",
    )

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "error": "Model output was not valid JSON",
            "raw_output": raw,
        }


# --------------------------------------------------
# End-to-end demo
# --------------------------------------------------

def run_demo():
    print("\nAI-Assisted Letter of Credit Document Examination")
    print("=" * 55)

    note = input("\nEnter an examiner note:\n> ").strip()

    if not note:
        print("No examiner note supplied.")
        return

    print("\n1. Compliance classification")
    classification = classify_case(note)
    print(f"Result: {classification}")

    print("\n2. Relevant LC evidence")
    hits = retrieve(note)

    for i, hit in enumerate(hits, start=1):
        print(
            f"{i}. {hit['name']} "
            f"(similarity={hit['score']:.3f})"
        )
        print(f"   {hit['text']}")

    print("\n3. Structured discrepancy output")
    structured = extract_discrepancy(note)
    print(json.dumps(structured, indent=2))

    print("\n4. Grounded evidence summary")
    answer, _ = grounded_answer(
        "What evidence is relevant to this examiner note?"
    )
    print(answer)

    print("\nHuman review is recommended before any final trade-finance decision.")


if __name__ == "__main__":
    run_demo()
