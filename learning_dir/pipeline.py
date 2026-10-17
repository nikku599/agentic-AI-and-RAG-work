from openai import AsyncOpenAI
from models import Question, Answer, Token
from dotenv import load_dotenv


load_dotenv()
async_openai_client = AsyncOpenAI()

async def ask_llm(question : Question) -> Answer:
    response = await async_openai_client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an experienced professor. "
                    "Answer the question accurately and clearly. "
                    "Estimate your confidence in the factual correctness "
                    "of your answer between 0 and 1. "
                    "Return both fields in the required schema."
                ),
            },
            {"role":"user", "content": question.text}
        ],
        response_format=Answer,
        temperature=0.4
    )
    return response.choices[0].message.parsed

async def ask_llm_stream(q: Question):
    stream = await async_openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": q.text}
        ],
        stream=True,
    )

    async for chunk in stream:
        text = chunk.choices[0].delta.content

        if text:
            yield text

