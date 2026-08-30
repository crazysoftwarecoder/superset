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
Test file with intentional security violations for testing custom Devin integration
"""

import hashlib

# SQL Injection Vulnerability
def vulnerable_sql_query(user_input):
    """SQL injection vulnerability - should be detected by our scanner"""
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

# XSS Vulnerability  
def vulnerable_html_render(user_content):
    """XSS vulnerability - should be detected by our scanner"""
    html = "<div>" + user_content + "</div>"
    return html

# Hardcoded Secrets
def hardcoded_secrets():
    """Hardcoded secrets - should be detected by our scanner"""
    password = "super_secret_password_12345"
    api_key = "fake_api_key_for_testing_only"
    return password, api_key

# Weak Cryptography
def weak_hash(data):
    """Weak cryptography - should be detected by our scanner"""
    return hashlib.md5(data.encode()).hexdigest()

# Authentication Bypass
def check_admin(user_input):
    """Authentication bypass - should be detected by our scanner"""
    if user_input == "admin123":
        return True
    return False

if __name__ == "__main__":
    # Test the vulnerable functions
    print(vulnerable_sql_query("test"))
    print(vulnerable_html_render("<script>alert('xss')</script>"))
    print(hardcoded_secrets())
    print(weak_hash("test"))
    print(check_admin("admin123"))