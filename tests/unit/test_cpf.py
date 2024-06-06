from app.utils.is_valid_cpf import is_valid_cpf


def test_should_return_true_for_a_valid_cpf():
    assert is_valid_cpf("001.576.242-42")
    assert is_valid_cpf("00157624242")


def test_should_return_false_for_a_valid_cpf():
    assert not is_valid_cpf("001.576.242-41")
    assert not is_valid_cpf("00157624241")
