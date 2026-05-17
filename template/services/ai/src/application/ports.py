from abc import ABC, abstractmethod

from domain.models import PromptRequest, PromptResult


class LLMProvider(ABC):
    @abstractmethod
    def complete(self, request: PromptRequest) -> PromptResult:
        raise NotImplementedError
