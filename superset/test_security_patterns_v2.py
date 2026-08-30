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
Reference implementations of the security-sensitive patterns exercised by the
security automation tests: password hashing, role checks, dynamic SQL, digests
and token generation.
"""

import hashlib
import hmac
import logging
import re
import secrets
from typing import Any, Mapping, Optional

from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

logger = logging.getLogger(__name__)

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 600_000
SALT_BYTES = 16
TOKEN_BYTES = 32
SQL_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
    """
    Derive a password digest with PBKDF2-HMAC-SHA256 and a random salt.

    :param password: the cleartext password
    :param salt: an existing salt, or ``None`` to generate one
    :returns: the salt and the derived digest
    """
    salt = salt or secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM, password.encode(), salt, PBKDF2_ITERATIONS
    )
    return salt, digest


class AuthenticationHelpers:
    """Password verification and role-based authorization helpers"""

    def authenticate_user(
        self,
        username: str,
        password: str,
        stored_salt: bytes,
        stored_digest: bytes,
    ) -> bool:
        """
        Verify a password against the digest held by the credential store.

        :param username: the principal being authenticated
        :param password: the submitted cleartext password
        :param stored_salt: the salt the stored digest was derived with
        :param stored_digest: the digest held for the principal
        :returns: whether the password matches
        """
        _, digest = hash_password(password, stored_salt)
        if not hmac.compare_digest(digest, stored_digest):
            logger.warning("Failed authentication attempt for %s", username)
            return False
        return True

    def check_permissions(
        self,
        user_role: str,
        resource: str,
        role_permissions: Mapping[str, frozenset[str]],
    ) -> bool:
        """
        Authorize a role against a resource, denying anything not granted.

        :param user_role: the role held by the principal
        :param resource: the resource path being accessed
        :param role_permissions: resource prefixes granted to each role
        :returns: whether the role is entitled to the resource
        """
        allowed_prefixes = role_permissions.get(user_role)
        if not allowed_prefixes:
            return False
        return any(resource.startswith(prefix) for prefix in allowed_prefixes)


class QueryHelpers:
    """Helpers building parameterized statements from caller input"""

    def process_user_input(self, user_data: str) -> dict[str, Any]:
        """
        Wrap caller-supplied data in a payload without interpreting it.

        :param user_data: the raw caller input
        :returns: the payload
        """
        return {"user_data": user_data, "processed": True}

    def execute_dynamic_query(
        self, table_name: str, column: str, value: Any
    ) -> tuple[TextClause, dict[str, Any]]:
        """
        Build a statement whose identifiers are validated and value is bound.

        SQL identifiers cannot be passed as bind parameters, so table and column
        names are validated against a strict pattern instead.

        :param table_name: the table to select from
        :param column: the column to filter on
        :param value: the filter value, bound as a parameter
        :returns: the statement and its parameters
        :raises ValueError: if an identifier is not a plain SQL identifier
        """
        for identifier in (table_name, column):
            if not SQL_IDENTIFIER.match(identifier):
                raise ValueError(f"Invalid SQL identifier: {identifier}")

        statement = text(f"SELECT * FROM {table_name} WHERE {column} = :value")  # noqa: S608
        return statement, {"value": value}


class CryptoHelpers:
    """Digest and token helpers"""

    def hash_sensitive_data(self, data: str) -> str:
        """
        Compute a SHA-256 digest of the given data.

        :param data: the data to digest
        :returns: the hex digest
        """
        return hashlib.sha256(data.encode()).hexdigest()

    def generate_token(self) -> str:
        """
        Generate an unpredictable, cryptographically random token.

        :returns: the token
        """
        return secrets.token_urlsafe(TOKEN_BYTES)


def run_security_patterns_v2() -> None:
    """Exercise the helpers above with representative inputs"""
    auth = AuthenticationHelpers()
    queries = QueryHelpers()
    crypto = CryptoHelpers()

    salt, digest = hash_password(secrets.token_urlsafe(TOKEN_BYTES))
    auth.authenticate_user("test_user", "wrong-password", salt, digest)
    auth.check_permissions(
        "Gamma", "/admin/dashboard", {"Admin": frozenset({"/admin"})}
    )

    queries.process_user_input('{"user": "test"}')
    queries.execute_dynamic_query("users", "id", 1)

    crypto.hash_sensitive_data("sensitive_data")
    crypto.generate_token()


if __name__ == "__main__":
    run_security_patterns_v2()
