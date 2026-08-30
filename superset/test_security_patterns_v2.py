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
Test file with intentional security vulnerabilities v2 for testing Devin security automation.
This file contains different code-level security issues than the first test.
"""

import logging
from typing import Dict, Any, Optional
import hashlib

logger = logging.getLogger(__name__)


class AuthenticationVulnerabilities:
    """Class with intentional authentication vulnerabilities for testing"""
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """
        INTENTIONAL SECURITY VULNERABILITY: Weak password hashing
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: Weak hash for password (not production-grade)
        password_hash = hashlib.md5(password.encode()).hexdigest()
        
        # VULNERABLE: Hardcoded admin password
        admin_password = "admin123456"
        
        # This would be the vulnerable authentication logic
        # if password_hash == stored_hash:
        #     return True
        return password_hash == admin_password
    
    def check_permissions(self, user_role: str, resource: str) -> bool:
        """
        INTENTIONAL SECURITY VULNERABILITY: Authorization bypass
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: Direct string comparison for role check
        if user_role == "admin":
            return True
        
        # VULNERABLE: No proper permission checking
        # if resource.startswith("/admin"):
        #     return user_role == "admin"
        return True


class DataValidationVulnerabilities:
    """Class with intentional data validation vulnerabilities for testing"""
    
    def process_user_input(self, user_data: str) -> Dict[str, Any]:
        """
        INTENTIONAL SECURITY VULNERABILITY: Unsafe data processing
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: No proper input validation
        # In real code: should validate user_data format first
        return {"user_data": user_data, "processed": True}
    
    def execute_dynamic_query(self, table_name: str, condition: str) -> str:
        """
        INTENTIONAL SECURITY VULNERABILITY: Dynamic SQL construction
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: Direct string concatenation for SQL
        query = f"SELECT * FROM {table_name} WHERE {condition}"
        
        # This would be the vulnerable SQL execution
        # result = db.session.execute(text(query))
        return query


class CryptoVulnerabilities:
    """Class with intentional cryptographic vulnerabilities for testing"""
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """
        INTENTIONAL SECURITY VULNERABILITY: Weak encryption
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: MD5 for data encryption (not encryption, but weak)
        encrypted = hashlib.md5(data.encode()).hexdigest()
        
        # VULNERABLE: No salt, no proper encryption
        return encrypted
    
    def generate_token(self, user_id: str) -> str:
        """
        INTENTIONAL SECURITY VULNERABILITY: Predictable token generation
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: Simple hash without randomness
        token = hashlib.md5((user_id + "static_salt").encode()).hexdigest()
        
        # VULNERABLE: No expiration, no randomness
        return token


def create_test_vulnerabilities_v2():
    """Function to demonstrate intentional security vulnerabilities v2"""
    auth = AuthenticationVulnerabilities()
    data = DataValidationVulnerabilities()
    crypto = CryptoVulnerabilities()
    
    # Test authentication vulnerabilities
    auth.authenticate_user("test_user", "password123")
    auth.check_permissions("user", "/admin/dashboard")
    
    # Test data validation vulnerabilities
    data.process_user_input('{"user": "test"}')
    data.execute_dynamic_query("users", "id = 1")
    
    # Test cryptographic vulnerabilities
    crypto.encrypt_sensitive_data("sensitive_data")
    crypto.generate_token("user_123")


if __name__ == "__main__":
    create_test_vulnerabilities_v2()
# Testing improved GitHub reporting
