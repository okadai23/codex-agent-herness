from application.ports import LLMProvider
from domain.models import PromptRequest, PromptResult


class GenerateAnswerUseCase:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    def run(self, user_input: str) -> PromptResult:
        return self._provider.complete(PromptRequest(user_input=user_input))
