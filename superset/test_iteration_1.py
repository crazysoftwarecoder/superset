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
Test file iteration 1 - Simple security vulnerabilities for testing our system
"""

import hashlib

def vulnerable_sql_query(user_input):
    """SQL injection vulnerability"""
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

def vulnerable_password_hash(password):
    """Weak password hashing"""
    return hashlib.md5(password.encode()).hexdigest()

def hardcoded_api_key():
    """Hardcoded API key"""
    api_key = "sk_test_1234567890abcdefghijklmnop"
    return api_key

if __name__ == "__main__":
    print(vulnerable_sql_query("test"))
    print(vulnerable_password_hash("password123"))
    print(hardcoded_api_key())
