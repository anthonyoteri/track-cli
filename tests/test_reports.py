from datetime import timedelta

import mock
import pytest

from track import report


@pytest.mark.parametrize("year", [None, 2019])
def test_report_for_week(year, mocker):
    today = mocker.patch("pendulum.today")
    today.return_value.year = 2019

    get = mocker.patch("requests.get")

    get.return_value.json.return_value = {
        "days": [
            {"date": "2019-07-01", "records": {}, "total": 0},
            {
                "date": "2019-07-02",
                "records": {"foo": 10, "bar": 20, "baz": 30},
                "total": 60,
            },
            {"date": "2019-07-03", "records": {}, "total": 0},
            {"date": "2019-07-04", "records": {}, "total": 0},
            {"date": "2019-07-05", "records": {}, "total": 0},
            {"date": "2019-07-06", "records": {}, "total": 0},
            {"date": "2019-07-07", "records": {}, "total": 0},
        ],
        "projects": ["bar", "baz", "foo"],
        "week_number": "2019-W05",
    }

    tabulate = mocker.patch("tabulate.tabulate")

    report.report(host="abc", week=5, year=year)

    if year is None:
        assert today.called

    tabulate.assert_called_once_with(
        [
            ["bar", "", timedelta(0, 20), "", "", "", "", ""],
            ["baz", "", timedelta(0, 30), "", "", "", "", ""],
            ["foo", "", timedelta(0, 10), "", "", "", "", ""],
            [
                "",
                timedelta(0),
                timedelta(0, 60),
                timedelta(0),
                timedelta(0),
                timedelta(0),
                timedelta(0),
                timedelta(0),
            ],
        ],
        headers=[
            "PROJECT",
            "2019-07-01",
            "2019-07-02",
            "2019-07-03",
            "2019-07-04",
            "2019-07-05",
            "2019-07-06",
            "2019-07-07",
        ],
    )


def test_main(mocker):

    report_fn = mocker.patch("track.report.report")

    args = mocker.Mock()
    args.month = 7
    args.year = 2019
    args.host = "abc"

    report.main(args)

    calls = [
        mock.call(host="abc", week=27, year=2019, category=None),
        mock.call(host="abc", week=28, year=2019, category=None),
        mock.call(host="abc", week=29, year=2019, category=None),
        mock.call(host="abc", week=30, year=2019, category=None),
        mock.call(host="abc", week=31, year=2019, category=None),
    ]

    assert report_fn.has_calls(calls)
