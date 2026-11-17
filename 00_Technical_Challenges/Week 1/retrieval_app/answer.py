"""Stage 5: turn retrieved chunks into an answer.

YOUR CODE GOES HERE. The prompt is yours to write — it is the cheapest thing
in the pipeline to change and often the most effective.
"""

from .index import Hit, client

CHAT_MODEL = "gpt-4.1-mini"
FALL_BACK = "I don't have information about that in my knowledge base."
SYSTEM_PROMPT = f"""You are a helpful assistant that answers questions based strictly on provided context.

    Instructions:
    - Only answer questions using information from the provided context
    - Be accurate and cite specific parts of the context with [chunk N] when possible
    - If the context does not contain the answer, reply with exactly: "{FALL_BACK}"
    - Avoid making up information or providing personal opinions
    - Only use the provided context. Do not use external knowledge.
    - Include a gentle reminder that users should consult professionals for appropriate advice when relevant.
    - Only provide answers when you are confident the context supports your response."""


def build_messages(question: str, hits: list[Hit]) -> list[dict]:
    """Assemble the messages list sent to the chat model.

    Args:
        question: the user's question.
        hits: what search() returned. May be empty.

    Returns:
        A list of {"role": ..., "content": ...} dicts — a system message
        setting the rules, and a user message carrying the context and the
        question.

    Three things your prompt has to decide, and they are real decisions:
      1. How do you label each chunk in the context so the model can refer to
         it? (hit.chunk_id exists for this.)
      2. What should it do when the context does not contain the answer? Say
         so explicitly, or it will answer from the nearest chunk regardless.
      3. What happens when `hits` is empty? Write that branch deliberately.

    Hint: Session 2's RAG_SYSTEM_TEMPLATE is a good starting point, and a
    better one once you have read Step 3's failures and edited it.
    """

    context_parts = [f"[chunk {hit.chunk_id}]\n{hit.text}" for hit in hits]
    context = "\n\n".join(context_parts)
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]


def answer(question: str, hits: list[Hit]) -> str:
    """Call the chat model and return its reply as a string.

    Hint: `client().chat.completions.create(model=CHAT_MODEL, messages=...)`,
    then dig out `.choices[0].message.content`. Look up what `temperature`
    does to your results when you run the same question twice.
    """
    if not hits:
        return FALL_BACK
    messages = build_messages(question, hits)
    response = client().chat.completions.create(model=CHAT_MODEL, messages=messages, temperature=0)
    return response.choices[0].message.content