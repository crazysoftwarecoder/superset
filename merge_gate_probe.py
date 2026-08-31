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
import sqlite3
from typing import Any


def lookup(name: str) -> list[Any]:
    """
    Return the rows of table ``t`` whose ``name`` column equals ``name``.

    The value is bound as a query parameter so it is never interpolated into
    the SQL text.
    """
    with sqlite3.connect("x.db") as connection:
        cursor = connection.execute("SELECT * FROM t WHERE name = ?", (name,))
        return cursor.fetchall()
