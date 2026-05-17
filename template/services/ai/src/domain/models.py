from dataclasses import dataclass


@dataclass(frozen=True)
class PromptRequest:
    user_input: str


@dataclass(frozen=True)
class PromptResult:
    text: str
