from datetime import timedelta
import logging

import pendulum
import requests
import tabulate


log = logging.getLogger(__name__)


def report(
    *, host: str, year: int = None, week: int = None, category: str = None
) -> None:

    if year is None:
        year = pendulum.today().year

    if week is None:
        week = pendulum.today().week_of_year

    url = f"http://{host}/api/reports/week/{year}/{week}/"
    if category is not None:
        url = f"{url}{category}/"

    resp = requests.get(url)
    resp.raise_for_status()

    body = resp.json()
    print("Report for Week %s" % body["week_number"])
    if category is not None:
        print("Filtered by category %s" % body["category"])

    projects = body["projects"]

    rows = []
    headers = ["PROJECT"] + [day["date"] for day in body["days"]]
    for project in projects:
        row = [project]
        for day in body["days"]:
            value = ""
            if project in day["records"]:
                value = timedelta(seconds=day["records"][project])
            row.append(value)
        rows.append(row)
    rows.append(
        [""] + [timedelta(seconds=day["total"]) for day in body["days"]]
    )
    print(tabulate.tabulate(rows, headers=headers))


def main(args):

    if args.month is not None:
        year = args.year or pendulum.today().year
        date_in_month = pendulum.datetime(year, args.month, 1)
        for week in (
            date_in_month.end_of("month") - date_in_month.start_of("month")
        ).range("weeks"):
            report(
                host=args.host,
                week=week.week_of_year,
                year=year,
                category=args.category,
            )
            print("\n")
        return

    if args.week is not None:
        if not 0 < args.week <= 53:
            raise Exception("Invalid week number %s" % args.week)

    report(
        host=args.host, week=args.week, year=args.year, category=args.category
    )
