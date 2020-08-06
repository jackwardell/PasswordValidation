from password_validation import PasswordPolicy


def test_simple_case():
    policy = PasswordPolicy()
    result = policy.test_password("hello")
    assert result

    result = policy.test_password("hsdhkhasjdhasd")
    assert not result
