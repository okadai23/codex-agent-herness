from fastapi import FastAPI

from adapters.fake_provider import FakeLLMProvider
from application.use_cases import GenerateAnswerUseCase

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate")
def generate(payload: dict[str, str]) -> dict[str, str]:
    use_case = GenerateAnswerUseCase(FakeLLMProvider())
    result = use_case.run(payload.get("input", ""))
    return {"output": result.text}
