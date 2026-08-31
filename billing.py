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
from typing import Any, Optional


def get_invoice(invoice_id: str) -> Optional[tuple[Any, ...]]:
    """
    Fetch an invoice by id.

    :param invoice_id: identifier of the invoice to fetch
    :returns: the matching invoice row, or ``None`` if there is none
    """
    with sqlite3.connect("billing.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id, amount, customer FROM invoices WHERE id = ?",
            (invoice_id,),
        )
        return cur.fetchone()
