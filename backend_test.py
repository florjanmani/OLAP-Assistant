#!/usr/bin/env python3
"""
OLAP Assistant Backend API Testing Suite
Tests all backend endpoints for the OLAP Assistant application
"""

import requests
import sys
import json
import time
from datetime import datetime

class OLAPBackendTester:
    def __init__(self, base_url="https://bi-chat-tool.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.session_id = None
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {name} - PASSED")
        else:
            print(f"❌ {name} - FAILED: {details}")
        
        self.test_results.append({
            "test": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })

    def run_test(self, name, method, endpoint, expected_status, data=None, timeout=30):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
        headers = {'Content-Type': 'application/json'}

        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=timeout)
            else:
                self.log_test(name, False, f"Unsupported method: {method}")
                return False, {}

            success = response.status_code == expected_status
            
            if success:
                try:
                    response_data = response.json()
                    self.log_test(name, True, f"Status: {response.status_code}")
                    return True, response_data
                except json.JSONDecodeError:
                    self.log_test(name, True, f"Status: {response.status_code} (No JSON response)")
                    return True, {}
            else:
                error_msg = f"Expected {expected_status}, got {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    error_msg += f" - {response.text[:200]}"
                self.log_test(name, False, error_msg)
                return False, {}

        except requests.exceptions.Timeout:
            self.log_test(name, False, f"Request timeout after {timeout}s")
            return False, {}
        except requests.exceptions.ConnectionError:
            self.log_test(name, False, "Connection error - service may be down")
            return False, {}
        except Exception as e:
            self.log_test(name, False, f"Unexpected error: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test GET /api/ returns correct message"""
        success, response = self.run_test(
            "Root API Endpoint",
            "GET",
            "",
            200
        )
        
        if success and response.get("message") == "OLAP Assistant API":
            print("   ✓ Correct message returned")
            return True
        elif success:
            self.log_test("Root API Message Check", False, f"Expected 'OLAP Assistant API', got '{response.get('message')}'")
            return False
        return success

    def test_data_initialization(self):
        """Test POST /api/data/init initializes sample data"""
        success, response = self.run_test(
            "Data Initialization",
            "POST",
            "data/init",
            200
        )
        
        if success:
            record_count = response.get("record_count", 0)
            if record_count > 0:
                print(f"   ✓ Initialized {record_count} records")
                return True
            else:
                self.log_test("Data Init Record Count", False, f"Expected > 0 records, got {record_count}")
                return False
        return success

    def test_data_summary(self):
        """Test GET /api/data/summary returns data summary"""
        success, response = self.run_test(
            "Data Summary",
            "GET",
            "data/summary",
            200
        )
        
        if success:
            required_fields = ["total_records", "total_sales", "dimensions"]
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                print(f"   ✓ Total records: {response.get('total_records', 0)}")
                print(f"   ✓ Total sales: ${response.get('total_sales', 0):,.2f}")
                print(f"   ✓ Dimensions available: {len(response.get('dimensions', {}))}")
                return True
            else:
                self.log_test("Data Summary Fields", False, f"Missing fields: {missing_fields}")
                return False
        return success

    def test_chat_endpoint(self):
        """Test POST /api/chat processes natural language query"""
        test_query = "Break down Q4 sales by region"
        
        success, response = self.run_test(
            "Chat Endpoint - Natural Language Query",
            "POST",
            "chat",
            200,
            data={"message": test_query},
            timeout=60  # LLM calls can take longer
        )
        
        if success:
            # Check response structure
            required_fields = ["response", "session_id"]
            missing_fields = [field for field in required_fields if field not in response]
            
            if not missing_fields:
                self.session_id = response.get("session_id")
                print(f"   ✓ Session ID: {self.session_id}")
                print(f"   ✓ Response length: {len(response.get('response', ''))}")
                
                # Check if analysis result is present
                if response.get("analysis_result"):
                    analysis = response["analysis_result"]
                    print(f"   ✓ Analysis operation: {analysis.get('operation')}")
                    print(f"   ✓ Data rows returned: {analysis.get('row_count', 0)}")
                    return True
                else:
                    print("   ⚠ No analysis result returned (may be expected for some queries)")
                    return True
            else:
                self.log_test("Chat Response Fields", False, f"Missing fields: {missing_fields}")
                return False
        return success

    def test_chat_with_simple_query(self):
        """Test chat with a simple aggregation query"""
        test_query = "What's the total sales by category?"
        
        success, response = self.run_test(
            "Chat Endpoint - Simple Query",
            "POST",
            "chat",
            200,
            data={"message": test_query, "session_id": self.session_id},
            timeout=60
        )
        
        if success and response.get("analysis_result"):
            analysis = response["analysis_result"]
            if analysis.get("data") and len(analysis["data"]) > 0:
                print(f"   ✓ Returned {len(analysis['data'])} category results")
                return True
            else:
                self.log_test("Chat Analysis Data", False, "No data returned in analysis result")
                return False
        return success

    def test_olap_direct_query(self):
        """Test direct OLAP query endpoint"""
        query_data = {
            "operation": "aggregate",
            "dimensions": ["region"],
            "measures": ["sales_amount"],
            "filters": {"quarter": "Q4"}
        }
        
        success, response = self.run_test(
            "Direct OLAP Query",
            "POST",
            "olap/query",
            200,
            data=query_data
        )
        
        if success:
            if response.get("data") and len(response["data"]) > 0:
                print(f"   ✓ Returned {len(response['data'])} results")
                print(f"   ✓ Operation: {response.get('operation')}")
                return True
            else:
                self.log_test("OLAP Query Data", False, "No data returned")
                return False
        return success

    def test_sales_by_region(self):
        """Test sales by region endpoint"""
        success, response = self.run_test(
            "Sales by Region",
            "GET",
            "olap/sales-by-region?quarter=Q4",
            200
        )
        
        if success and response.get("data"):
            print(f"   ✓ Regional data returned: {len(response['data'])} regions")
            return True
        return success

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting OLAP Assistant Backend API Tests")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 60)

        # Test sequence
        tests = [
            self.test_root_endpoint,
            self.test_data_initialization,
            self.test_data_summary,
            self.test_chat_endpoint,
            self.test_chat_with_simple_query,
            self.test_olap_direct_query,
            self.test_sales_by_region,
        ]

        for test_func in tests:
            try:
                test_func()
                time.sleep(1)  # Brief pause between tests
            except Exception as e:
                print(f"❌ Test {test_func.__name__} crashed: {str(e)}")
                self.tests_run += 1

        # Print summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.tests_passed}/{self.tests_run} tests passed")
        
        if self.tests_passed == self.tests_run:
            print("🎉 All tests passed!")
            return 0
        else:
            print(f"⚠️  {self.tests_run - self.tests_passed} tests failed")
            return 1

    def get_test_report(self):
        """Get detailed test report"""
        return {
            "summary": f"Backend API testing completed: {self.tests_passed}/{self.tests_run} tests passed",
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "failed_tests": self.tests_run - self.tests_passed,
            "test_results": self.test_results,
            "timestamp": datetime.now().isoformat()
        }

def main():
    """Main test execution"""
    tester = OLAPBackendTester()
    
    try:
        exit_code = tester.run_all_tests()
        
        # Save test report
        report = tester.get_test_report()
        with open("/app/backend_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        return exit_code
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Test suite crashed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())