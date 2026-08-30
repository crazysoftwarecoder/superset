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

"""
Reference implementations of the safe counterparts to common web
vulnerabilities: parameterized SQL, output escaping, externalized secrets and
literal-only evaluation of untrusted input.
"""

import ast
import logging
import os
from typing import Any

from markupsafe import escape, Markup
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

logger = logging.getLogger(__name__)

ALLOWED_TABLES = frozenset({"users", "dashboards", "slices"})


class SecureQueryHandler:
    """Query handler demonstrating secure alternatives to unsafe patterns."""

    def build_user_query(
        self, user_id: int, table_name: str
    ) -> tuple[TextClause, dict[str, Any]]:
        """
        Build a parameterized query for a single row of an allowlisted table.

        Identifiers cannot be bound as parameters, so the table name is
        restricted to a fixed allowlist; the user-supplied value is bound.
        """
        if table_name not in ALLOWED_TABLES:
            raise ValueError(f"Unknown table: {table_name}")

        statement = text(f"SELECT * FROM {table_name} WHERE id = :user_id")  # noqa: S608
        return statement, {"user_id": user_id}

    def render_user_content(self, user_input: str) -> Markup:
        """Render user-supplied content with the input HTML-escaped."""
        return Markup("<div>{}</div>").format(escape(user_input))

    def get_api_credentials(self) -> dict[str, str]:
        """
        Read API credentials from the environment.

        Credentials are supplied by the operator at deployment time and are
        never stored in the source tree.
        """
        api_key = os.environ.get("SUPERSET_API_KEY")
        api_secret = os.environ.get("SUPERSET_API_SECRET")
        if not api_key or not api_secret:
            raise ValueError(
                "SUPERSET_API_KEY and SUPERSET_API_SECRET must be configured"
            )

        return {"api_key": api_key, "api_secret": api_secret}

    def process_user_data(self, data: str) -> Any:
        """
        Parse user-supplied data as a Python literal.

        ``ast.literal_eval`` evaluates only literals, so no attacker-controlled
        code can be executed.
        """
        try:
            return ast.literal_eval(data)
        except (SyntaxError, ValueError) as ex:
            raise ValueError("Payload is not a valid Python literal") from ex
