from application.ports import LLMProvider
from domain.models import PromptRequest, PromptResult


class FakeLLMProvider(LLMProvider):
    def complete(self, request: PromptRequest) -> PromptResult:
        return PromptResult(text=f"echo:{request.user_input}")
