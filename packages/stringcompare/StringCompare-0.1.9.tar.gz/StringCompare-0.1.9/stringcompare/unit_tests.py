import pytest
from .hashing_search import hashing_search
from .linear_search import linear_search


@pytest.mark.parametrize("a, b", [('aaa', 'aaa'),
                                ('abcdefg', 'abcdefg'),
                                ('abcd', 'abcd'),
                                ('1111', '1111')])
def test_string_compare_true(a:str, b:str):
    assert hashing_search(a, b) == True
    assert linear_search(a, b) == True


@pytest.mark.parametrize('a, b', [('abcd', 'bcda'),
                                    ('qwer', 'sdfw'),
                                    ('dfgdgfd', 'df'),
                                    ('12334', '12344')])
def test_string_compare_false(a:str, b:str):
    assert hashing_search(a, b) == False
    assert linear_search(a, b) == False
