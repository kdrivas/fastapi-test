import pytest
from model.utils import unicodeToAscii


@pytest.mark.parametrize(
    "str_input, expected_output",
    [
        pytest.param("name1", "name", id="test_1"),
        pytest.param("name2", "name", id="test_2"),
    ]
)
def test_drop_cols_transformer(
    str_input: str, expected_output: str,
):
    str_output = unicodeToAscii(str_input)

    assert str_output == expected_output
