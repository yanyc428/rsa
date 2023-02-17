import fastapi
from fastapi.middleware.cors import CORSMiddleware
from rsa import generate_key
from text import text_encode, text_decode
app = fastapi.FastAPI()

# 使用中间件以拓展跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/generate')
def generate():
    return generate_key()


@app.post('/api/encode')
def encode(s: str, key: str):
    return text_encode(s, key)


@app.post('/api/decode')
def decode(s: str, key: str):
    return text_decode(s, key)
