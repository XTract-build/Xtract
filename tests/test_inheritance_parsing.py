import pytest
from xtract.transpiler import Transpiler

@pytest.fixture
def transpiler():
    return Transpiler()

def test_parse_inheritance_single(transpiler):
    content = "contract MyContract is Parent {}"
    assert transpiler.parse_inheritance(content) == ["Parent"]

def test_parse_inheritance_multiple(transpiler):
    content = "contract MyContract is Parent1, Parent2, Parent3 {}"
    assert transpiler.parse_inheritance(content) == ["Parent1", "Parent2", "Parent3"]

def test_parse_inheritance_with_constructor_args(transpiler):
    content = "contract MyContract is Parent1(100), Parent2(\"hello\"), Parent3(1, 2) {}"
    assert transpiler.parse_inheritance(content) == ["Parent1", "Parent2", "Parent3"]

def test_parse_inheritance_with_unusual_whitespace(transpiler):
    content = """
    contract   MyContract    is
        Parent1,
        Parent2,
        Parent3
    {
    """
    assert transpiler.parse_inheritance(content) == ["Parent1", "Parent2", "Parent3"]

def test_parse_inheritance_with_tabs(transpiler):
    content = "contract\tMyContract\tis\tParent1,\tParent2\t{"
    assert transpiler.parse_inheritance(content) == ["Parent1", "Parent2"]

def test_parse_inheritance_with_comments_single_line(transpiler):
    content = """
    contract MyContract is // some comment
        Parent1, // another comment
        Parent2
    {
    """
    assert transpiler.parse_inheritance(content) == ["Parent1", "Parent2"]

def test_parse_inheritance_with_comments_multi_line(transpiler):
    content = """
    contract MyContract is /* multi
    line */ Parent1, /* comment */ Parent2 {
    """
    assert transpiler.parse_inheritance(content) == ["Parent1", "Parent2"]

def test_parse_inheritance_none(transpiler):
    content = "contract MyContract {}"
    assert transpiler.parse_inheritance(content) == []

def test_parse_inheritance_abstract(transpiler):
    content = "abstract contract MyContract is Parent {}"
    assert transpiler.parse_inheritance(content) == ["Parent"]

def test_parse_inheritance_with_interface(transpiler):
    # Interfaces don't use 'is' for inheritance in the same way, but let's see
    content = "interface IMyInterface {}"
    assert transpiler.parse_inheritance(content) == []

def test_parse_inheritance_complex_args(transpiler):
    # Testing nested parentheses in constructor args (though unusual in Solidity inheritance)
    content = "contract MyContract is Parent(call()) {}"
    assert transpiler.parse_inheritance(content) == ["Parent"]
