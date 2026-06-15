from openai import OpenAI

from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, OPENROUTER_MODEL


def get_client() -> OpenAI:
    if not OPENROUTER_API_KEY:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )


def chat_completion(
    messages: list[dict[str, str]],
    *,
    model: str | None = None,
    temperature: float = 0.4,
) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=model or OPENROUTER_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
