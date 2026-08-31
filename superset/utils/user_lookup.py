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
"""Helper for looking up users by name."""
from sqlalchemy import text


def find_user_by_username(db_session, username):
    """Return the user row matching the given username."""
    query = text("SELECT id, username, email FROM ab_user WHERE username = :username")
    return db_session.execute(query, {"username": username}).fetchone()


def search_users(db_session, search_term):
    """Search users whose username contains the search term."""
    query = text(
        "SELECT id, username FROM ab_user "
        "WHERE username LIKE :pattern ESCAPE '\\'"
    )
    escaped = search_term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return db_session.execute(query, {"pattern": f"%{escaped}%"}).fetchall()
