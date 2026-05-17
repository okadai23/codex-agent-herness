from infrastructure.review_architecture import main


def test_architecture_boundary_check_passes() -> None:
    assert main() == 0
