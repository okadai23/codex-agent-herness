from adapters.fake_provider import FakeLLMProvider
from application.use_cases import GenerateAnswerUseCase


def test_use_case_uses_fake_provider_without_external_call() -> None:
    use_case = GenerateAnswerUseCase(FakeLLMProvider())

    result = use_case.run("hello")

    assert result.text == "echo:hello"
