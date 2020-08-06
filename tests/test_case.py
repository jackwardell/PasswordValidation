from password_entropy import PasswordPolicy


def test_simple_case():
    policy = PasswordPolicy()
    result = policy.test_password("hello")
    assert result

    result = policy.test_password("hsdhkhasjdhasd")
    assert not result
