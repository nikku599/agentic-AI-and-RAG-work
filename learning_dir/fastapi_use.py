import asyncio

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from models import Question, Answer
from pipeline import ask_llm, ask_llm_stream

app = FastAPI()


status_ok = {"status":"running"}

@app.get('/health')
async def health_function():
    return status_ok


@app.post('/ask')
async def ask_ai(q : Question):
    return await ask_llm(q)

async def _stream_after_llm_call(q:Question):
    ans = await ask_llm(q)
    for word in ans.text.split(" "):
        yield word + " "
        await asyncio.sleep(0.1)
        
@app.post('/ask-stream')
async def ask_ai_stream(q:Question):
    return StreamingResponse(ask_llm_stream(q), media_type='text/plain')