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
Test file with intentional security vulnerabilities for testing Devin security automation.
This file contains code-level security issues that should be detected and fixed.
"""

import logging
from typing import Dict, Any, Optional
from sqlalchemy import text

logger = logging.getLogger(__name__)


class VulnerableQueryHandler:
    """Query handler with intentional security vulnerabilities for testing"""
    
    def execute_user_query(self, user_id: str, table_name: str) -> Dict[str, Any]:
        """
        INTENTIONAL SECURITY VULNERABILITY: SQL Injection via string concatenation
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: String concatenation in SQL query
        query = "SELECT * FROM " + table_name + " WHERE id = " + user_id
        
        # This would be the vulnerable execution in real code
        # result = db.session.execute(text(query))
        
        return {"query": query, "result": "vulnerable_pattern"}
    
    def render_user_content(self, user_input: str) -> str:
        """
        INTENTIONAL SECURITY VULNERABILITY: XSS via innerHTML
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: Direct innerHTML assignment with user input
        # In real code: element.innerHTML = user_input
        content = f"<div>{user_input}</div>"
        
        return content
    
    def get_api_credentials(self) -> Dict[str, str]:
        """
        INTENTIONAL SECURITY VULNERABILITY: Hardcoded credentials
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: Hardcoded API credentials (obviously fake for testing)
        credentials = {
            "api_key": "test_api_key_not_real_12345",
            "api_secret": "test_secret_not_real_67890"
        }
        
        return credentials
    
    def process_user_data(self, data: str) -> str:
        """
        INTENTIONAL SECURITY VULNERABILITY: Unsafe eval
        This is deliberately vulnerable for testing the security scanner.
        """
        # VULNERABLE: eval() with user data
        # In real code: result = eval(data)
        return f"Would evaluate: {data}"


def create_test_vulnerabilities() -> None:
    """Function to demonstrate intentional security vulnerabilities"""
    handler = VulnerableQueryHandler()
    
    # Test SQL injection pattern
    handler.execute_user_query("1", "users")
    
    # Test XSS pattern
    handler.render_user_content("<script>alert('xss')</script>")
    
    # Test hardcoded secrets pattern
    handler.get_api_credentials()
    
    # Test eval pattern
    handler.process_user_data("__import__('os').system('ls')")


if __name__ == "__main__":
    create_test_vulnerabilities()
# Added line to trigger webhook
# Another test line
# Final test line
