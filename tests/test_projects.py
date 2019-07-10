import json

from track import project


def test_create(mocker):
    post = mocker.patch("requests.post")

    project.create(host="abc", name="def", description="ghi")

    post.assert_called_once_with(
        "http://abc/api/projects/", data={"name": "def", "description": "ghi"}
    )


def test_get(mocker):
    get = mocker.patch("requests.get")
    get.return_value.json.return_value = {"foo": "bar"}

    result = project.get(host="abc", name="def")

    get.assert_called_once_with("http://abc/api/projects/def/")
    assert result == json.dumps({"foo": "bar"}, indent=2)


def test_delete(mocker):
    delete = mocker.patch("requests.delete")

    project.delete(host="abc", name="def")

    delete.assert_called_once_with("http://abc/api/projects/def/")


def test_list(mocker):
    get = mocker.patch("requests.get")
    get.return_value.json.return_value = {"results": [{"name": "foo"}]}

    result = project.list(host="abc")

    get.assert_called_once_with("http://abc/api/projects/")
    assert result == ["foo"]


def test_update_name(mocker):
    patch = mocker.patch("requests.patch")

    project.update(host="abc", name="def", new_name="ghi")

    patch.assert_called_once_with(
        "http://abc/api/projects/def/", data={"name": "ghi"}
    )


def test_update_description(mocker):
    patch = mocker.patch("requests.patch")

    project.update(host="abc", name="def", description="ghi")

    patch.assert_called_once_with(
        "http://abc/api/projects/def/", data={"description": "ghi"}
    )


def test_update_categories(mocker):
    patch = mocker.patch("requests.patch")

    project.update(host="abc", name="def", categories=["ghi"])

    patch.assert_called_once_with(
        "http://abc/api/projects/def/", data={"categories": ["ghi"]}
    )
