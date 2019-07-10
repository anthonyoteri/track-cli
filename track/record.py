#!/usr/bin/env python3

from datetime import datetime
import json
import logging
from typing import Optional

import pendulum
import requests

log = logging.getLogger(__name__)


def list(
    *,
    host: str,
    begin: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    url = f"http://{host}/api/records/"

    resp = requests.get(url)
    resp.raise_for_status()

    body = resp.json()
    return body["results"]


def start(*, host: str, project: str, at: Optional[datetime] = None):
    url = f"http://{host}/api/records/"

    if at is None:
        at = pendulum.now("UTC")
    else:
        at = pendulum.parse(at)

    resp = requests.post(
        url, data={"project": project, "start_time": at.isoformat()}
    )
    resp.raise_for_status()


def stop(*, host: str, at: Optional[datetime] = None):
    url = f"http://{host}/api/records/active/"

    if at is None:
        at = pendulum.now("UTC")
    else:
        at = pendulum.parse(at)

    resp = requests.get(url)
    if resp.status_code == 404:
        log.warning("There is no active record")
        return

    resp.raise_for_status()
    active = resp.json()

    resp = requests.post(
        url, data={"project": active["project"], "stop_time": at.isoformat()}
    )
    resp.raise_for_status()


def main(args):

    if args.start:
        start(host=args.host, project=args.start, at=args.arg)
        return

    if args.stop:
        stop(host=args.host, at=args.arg)
        return

    for record in list(host=args.host):
        print(json.dumps(record, indent=2))
