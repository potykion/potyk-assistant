import pytest

from kys_in_rest.core.tg_utils import AskForData


def test_add_new(rest_factory):
    add_new_rest = rest_factory.make_add_new_restaurant()
    repo = rest_factory.make_sqlite_rest_repo()

    with pytest.raises(AskForData):
        add_new_rest.do()

    rest, created = repo.get_or_create_draft()
    assert rest
    assert not created

    rest = add_new_rest.do("test")

    assert rest["name"] == "test"
    assert rest["draft"] is False
