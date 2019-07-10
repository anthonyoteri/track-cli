#!/usr/bin/env python3

import argparse
import logging
from typing import List
import sys


from requests.exceptions import HTTPError
import requests

from .exceptions import MissingArgumentError
from . import category, project, record, report

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def list_projects(*, host: str) -> List[str]:
    url = f"http://{host}/api/projects/"

    resp = requests.get(url)
    resp.raise_for_status()

    projects = []
    body = resp.json()

    projects += [r["name"] for r in body["results"]]
    return projects


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-H", "--host", help="host:port", default="localhost:8888"
    )

    subparsers = parser.add_subparsers()

    categories_parser = subparsers.add_parser("categories")
    categories_parser.add_argument("-s", "--show")
    categories_parser.add_argument("-c", "--create")
    categories_parser.add_argument("-D", "--delete")
    categories_parser.add_argument("-r", "--rename")
    categories_parser.add_argument("-d", "--describe")
    categories_parser.add_argument("arg", nargs="?")
    categories_parser.set_defaults(func=category.main)

    projects_parser = subparsers.add_parser("projects")
    projects_parser.add_argument("-s", "--show")
    projects_parser.add_argument("-c", "--create")
    projects_parser.add_argument("-a", "--assign")
    projects_parser.add_argument("-D", "--delete")
    projects_parser.add_argument("-r", "--rename")
    projects_parser.add_argument("-d", "--describe")
    projects_parser.add_argument("arg", nargs="?")
    projects_parser.set_defaults(func=project.main)

    records_parser = subparsers.add_parser("records")
    records_parser.add_argument("-s", "--start")
    records_parser.add_argument("-p", "--stop", action="store_true")
    records_parser.add_argument("arg", nargs="?")
    records_parser.set_defaults(func=record.main)

    reports_parser = subparsers.add_parser("reports")
    reports_parser.add_argument("-y", "--year", type=int)
    reports_parser.add_argument("-w", "--week", type=int)
    reports_parser.add_argument("-c", "--category")
    reports_parser.add_argument("-m", "--month", type=int)
    reports_parser.set_defaults(func=report.main)

    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(2)

    try:
        args.func(args)
    except MissingArgumentError as err:
        parser.error("Missing argument: %s" % err)
    except HTTPError as err:
        log.error(err)
    except Exception as err:
        log.exception(err)
        sys.exit(1)


if __name__ == "__main__":
    main()
