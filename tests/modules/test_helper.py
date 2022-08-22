import pytest
import pandas as pd
import modules.helper as helper


def test_invert_dictionary():
    test = {1: "A", 2: "B", 3: "C"}
    result = {"A": 1, "B": 2, "C": 3}
    assert helper.invert_dictionary(test) == result

    with pytest.raises(ValueError):
        test = {1: "A", 2: "A", 3: "C"}
        helper.invert_dictionary(test)
