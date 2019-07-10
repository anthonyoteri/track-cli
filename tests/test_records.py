import pendulum
import pytest

from track import record


def test_list(mocker):
    get = mocker.patch("requests.get")
    get.return_value.json.return_value = {"results": ["def", "ghi"]}

    result = record.list(host="abc")

    get.assert_called_once_with("http://abc/api/records/")
    assert result == ["def", "ghi"]


@pytest.mark.parametrize("at", [None, "2015-05-01T00:09:30Z"])
def test_start(at, mocker):
    now = mocker.patch("pendulum.now")
    now.return_value = pendulum.datetime(2015, 5, 1, 0, 9, 30, tz="UTC")

    post = mocker.patch("requests.post")

    record.start(host="abc", project="def", at=at)

    if at is None:
        now.assert_called_once_with("UTC")
    post.assert_called_once_with(
        "http://abc/api/records/",
        data={"project": "def", "start_time": now.return_value.isoformat()},
    )


@pytest.mark.parametrize("status_code", [404, 200])
@pytest.mark.parametrize("at", [None, "2015-05-01T00:09:30Z"])
def test_stop(at, status_code, mocker):
    now = mocker.patch("pendulum.now")
    now.return_value = pendulum.datetime(2015, 5, 1, 0, 9, 30, tz="UTC")

    get = mocker.patch("requests.get")
    get.return_value.status_code = status_code
    get.return_value.json.return_value = {"project": "def"}

    post = mocker.patch("requests.post")

    record.stop(host="abc", at=at)

    if at is None:
        now.assert_called_once_with("UTC")
    get.assert_called_once_with("http://abc/api/records/active/")

    if status_code != 404:
        post.assert_called_once_with(
            "http://abc/api/records/active/",
            data={"project": "def", "stop_time": now.return_value.isoformat()},
        )
    else:
        assert not post.called
