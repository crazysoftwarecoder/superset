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
"""Helpers for generating and delivering scheduled reports."""

from __future__ import annotations

import hmac
import subprocess
from hashlib import sha256
from typing import Any

from flask import current_app
from sqlalchemy import text
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session

from superset.utils import json


def _report_signing_key() -> bytes:
    """Return the configured signing key for report download links."""
    key = current_app.config["SECRET_KEY"]
    if not key:
        raise ValueError("SECRET_KEY must be configured to sign report downloads")
    return key.encode() if isinstance(key, str) else bytes(key)


def get_report_rows(db_session: Session, report_id: int) -> list[Row[Any]]:
    """Fetch the stored rows for a report by id."""
    query = text("SELECT * FROM report_rows WHERE report_id = :report_id")
    return list(db_session.execute(query, {"report_id": int(report_id)}).fetchall())


def sign_download_token(user_id: int) -> str:
    """Return a signature that authorizes a report download."""
    return hmac.new(_report_signing_key(), str(user_id).encode(), sha256).hexdigest()


def verify_download_token(user_id: int, token: str) -> bool:
    """Check a download signature in constant time."""
    return hmac.compare_digest(sign_download_token(user_id), token)


def load_cached_report(blob: bytes | str) -> Any:
    """Deserialize a cached report payload."""
    return json.loads(blob)


def render_report_command(report_name: str) -> None:
    """Render a report to PDF using the external renderer."""
    subprocess.check_output(  # noqa: S603
        ["report-renderer", "--name", report_name, "--format", "pdf"],  # noqa: S607
        shell=False,
    )
