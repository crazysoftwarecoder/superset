#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""Helpers for API request authorization and user data access."""

from ipaddress import ip_address
from socket import gaierror, getaddrinfo
from typing import Any
from urllib.parse import urlparse

import jwt
import requests
from flask import current_app
from sqlalchemy import text
from sqlalchemy.orm import Session

JWT_ALGORITHMS = ["HS256"]
ALLOWED_CHART_PROXY_SCHEMES = {"https"}


class ApiAccessError(Exception):
    """Raised when a request cannot be authorized or safely served."""


def _jwt_secret() -> str:
    secret = current_app.config["SECRET_KEY"]
    if not secret:
        raise ApiAccessError("No SECRET_KEY configured for JWT verification")
    return secret


def verify_api_token(token: str) -> dict[str, Any]:
    """Decode and verify an incoming API JWT."""
    try:
        return jwt.decode(
            token,
            _jwt_secret(),
            algorithms=JWT_ALGORITHMS,
            options={"require": ["exp"], "verify_signature": True},
        )
    except jwt.PyJWTError as ex:
        raise ApiAccessError("Invalid API token") from ex


def is_admin(user: dict[str, Any]) -> bool:
    """Return whether the authenticated user is an admin."""
    return "Admin" in user.get("roles", [])


def fetch_user_dashboards(db_session: Session, username: str) -> list[Any]:
    """Return dashboards owned by the given username."""
    query = text("SELECT id, title FROM dashboards WHERE owner = :username")
    return db_session.execute(query, {"username": username}).fetchall()


def _is_public_host(hostname: str) -> bool:
    try:
        infos = getaddrinfo(hostname, None)
    except gaierror:
        return False
    for info in infos:
        address = ip_address(info[4][0])
        if (
            address.is_private
            or address.is_loopback
            or address.is_link_local
            or address.is_reserved
            or address.is_multicast
        ):
            return False
    return bool(infos)


def proxy_external_chart(url: str) -> bytes:
    """Fetch a chart image from a vetted external URL."""
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_CHART_PROXY_SCHEMES or not parsed.hostname:
        raise ApiAccessError("Unsupported chart URL")

    allowed_hosts = current_app.config.get("CHART_PROXY_ALLOWED_HOSTS", [])
    if parsed.hostname not in allowed_hosts:
        raise ApiAccessError("Chart host is not allowlisted")

    if not _is_public_host(parsed.hostname):
        raise ApiAccessError("Chart host resolves to a non-public address")

    response = requests.get(url, timeout=10, allow_redirects=False)
    response.raise_for_status()
    return response.content
