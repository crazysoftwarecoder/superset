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
Test file with security violations for testing enhanced Devin integration with fix suggestions
"""

import hashlib

# SQL Injection Vulnerability (different pattern)
def vulnerable_query_with_fstring(user_input):
    """SQL injection vulnerability with f-string"""
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    return query

# XSS Vulnerability with dangerous patterns
def render_user_content(user_content):
    """XSS vulnerability with dangerous patterns"""
    html = f"<div>{user_content}</div>"
    return html

# Hardcoded Secrets (different pattern)
def get_database_config():
    """Hardcoded database credentials"""
    config = {
        "host": "localhost",
        "user": "admin_user",
        "password": "admin_password_123",
        "database": "production_db"
    }
    return config

# Weak Cryptography with SHA1
def weak_hash_function(data):
    """Weak cryptography with SHA1"""
    return hashlib.sha1(data.encode()).hexdigest()

# Authentication Bypass with common pattern
def authenticate_user(username, password):
    """Authentication bypass with weak check"""
    if username == "admin" and password == "password":
        return True
    return False

if __name__ == "__main__":
    # Test the vulnerable functions
    print(vulnerable_query_with_fstring("test"))
    print(render_user_content("<script>alert('xss')</script>"))
    print(get_database_config())
    print(weak_hash_function("test"))
    print(authenticate_user("admin", "password"))