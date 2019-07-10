#!/usr/bin/env python3

import json
import logging
from typing import List, Optional

import requests

from .exceptions import MissingArgumentError

log = logging.getLogger(__name__)


def create(*, host: str, name: str, description: Optional[str] = None) -> None:
    url = f"http://{host}/api/projects/"

    body = {"name": name, "description": description}

    resp = requests.post(url, data=body)
    resp.raise_for_status()

    body = resp.json()


def get(*, host: str, name: str) -> str:

    url = f"http://{host}/api/projects/{name}/"

    resp = requests.get(url)
    resp.raise_for_status()

    body = resp.json()
    return json.dumps(body, indent=2)


def delete(*, host: str, name: str) -> None:
    url = f"http://{host}/api/projects/{name}/"

    resp = requests.delete(url)
    resp.raise_for_status()


def list(*, host: str) -> List[str]:
    url = f"http://{host}/api/projects/"

    resp = requests.get(url)
    resp.raise_for_status()

    categories = []
    body = resp.json()

    categories += [r["name"] for r in body["results"]]
    return categories


def update(
    *,
    host: str,
    name: str,
    new_name: Optional[str] = None,
    description: Optional[str] = None,
    categories: Optional[List[str]] = None,
) -> None:
    url = f"http://{host}/api/projects/{name}/"

    body = {}
    if new_name is not None:
        body["name"] = new_name

    if description is not None:
        body["description"] = description

    if categories is not None:
        body["categories"] = categories

    resp = requests.patch(url, data=body)
    resp.raise_for_status()


def main(args):

    if args.show:
        print(get(host=args.host, name=args.show))
        return

    if args.create:
        create(host=args.host, name=args.create, description=args.arg)
        return

    if args.assign:
        categories = []
        if args.arg:
            categories = args.arg.split(",")

        update(host=args.host, name=args.assign, categories=categories)
        return

    if args.delete:
        delete(host=args.host, name=args.delete)
        return

    if args.rename:
        if args.arg is None:
            raise MissingArgumentError("arg")
        update(host=args.host, name=args.rename, new_name=args.arg)
        return

    if args.describe:
        if args.arg is None:
            raise MissingArgumentError("arg")
        update(host=args.host, name=args.describe, description=args.arg)
        return

    for project in list(host=args.host):
        print(project)
