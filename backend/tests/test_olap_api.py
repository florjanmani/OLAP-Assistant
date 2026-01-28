"""
OLAP Assistant Backend API Tests
Tests all API endpoints for the OLAP Assistant application.
"""

import pytest
import requests
import os
import time

# Get base URL from environment
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestHealthCheck:
    """Health check endpoint tests"""
    
    def test_api_root_returns_message(self):
        """Test /api/ health check returns correct message"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "OLAP Assistant API"


class TestDataSummary:
    """Data summary endpoint tests"""
    
    def test_data_summary_returns_10000_plus_records(self):
        """Test /api/data/summary returns data with 10,000+ records"""
        response = requests.get(f"{BASE_URL}/api/data/summary")
        assert response.status_code == 200
        data = response.json()
        
        # Verify record count
        assert "total_records" in data
        assert data["total_records"] >= 10000, f"Expected 10000+ records, got {data['total_records']}"
        
        # Verify other summary fields
        assert "total_sales" in data
        assert "total_quantity" in data
        assert "avg_sale" in data
        assert "dimensions" in data
        
        # Verify dimensions structure
        dims = data["dimensions"]
        assert "regions" in dims
        assert "products" in dims
        assert "quarters" in dims
        assert "years" in dims
        
        # Verify dimension values
        assert len(dims["regions"]) == 5  # North, South, East, West, Central
        assert len(dims["products"]) == 8  # 8 products
        assert len(dims["quarters"]) == 4  # Q1-Q4
        assert len(dims["years"]) == 3  # 2022-2024


class TestOLAPEndpoints:
    """OLAP query endpoint tests"""
    
    def test_sales_by_region_returns_regional_breakdown(self):
        """Test /api/olap/sales-by-region returns regional sales breakdown"""
        response = requests.get(f"{BASE_URL}/api/olap/sales-by-region")
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "operation" in data
        assert "dimensions" in data
        assert "data" in data
        assert "row_count" in data
        
        # Verify we have 5 regions
        assert data["row_count"] == 5
        assert len(data["data"]) == 5
        
        # Verify each region has required fields
        for region_data in data["data"]:
            assert "region" in region_data
            assert "total_sales_amount" in region_data
            assert "total_quantity" in region_data
    
    def test_sales_by_region_with_quarter_filter(self):
        """Test /api/olap/sales-by-region with quarter filter"""
        response = requests.get(f"{BASE_URL}/api/olap/sales-by-region?quarter=Q4")
        assert response.status_code == 200
        data = response.json()
        
        assert data["row_count"] == 5
        assert data["filters"]["quarter"] == "Q4"
    
    def test_sales_by_product_returns_product_data(self):
        """Test /api/olap/sales-by-product returns product sales data"""
        response = requests.get(f"{BASE_URL}/api/olap/sales-by-product")
        assert response.status_code == 200
        data = response.json()
        
        # Verify structure
        assert "operation" in data
        assert "dimensions" in data
        assert "data" in data
        assert "row_count" in data
        
        # Verify we have 8 products
        assert data["row_count"] == 8
        assert len(data["data"]) == 8
        
        # Verify each product has required fields
        for product_data in data["data"]:
            assert "product" in product_data
            assert "total_sales_amount" in product_data
            assert "total_quantity" in product_data
    
    def test_sales_by_product_with_region_filter(self):
        """Test /api/olap/sales-by-product with region filter"""
        response = requests.get(f"{BASE_URL}/api/olap/sales-by-product?region=North")
        assert response.status_code == 200
        data = response.json()
        
        assert data["row_count"] == 8
        assert data["filters"]["region"] == "North"


class TestAgentEndpoints:
    """Agent status and capabilities endpoint tests"""
    
    def test_agents_status_returns_all_active(self):
        """Test /api/agents/status returns agent status"""
        response = requests.get(f"{BASE_URL}/api/agents/status")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all 4 agents are active
        expected_agents = ["dimension_navigator", "cube_operations", "kpi_calculator", "report_generator"]
        for agent in expected_agents:
            assert agent in data
            assert data[agent] == "active"
    
    def test_agents_capabilities_returns_capabilities(self):
        """Test /api/agents/capabilities returns agent capabilities"""
        response = requests.get(f"{BASE_URL}/api/agents/capabilities")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all agents have capabilities listed
        expected_agents = ["dimension_navigator", "cube_operations", "kpi_calculator", "report_generator"]
        for agent in expected_agents:
            assert agent in data
            assert isinstance(data[agent], list)
            assert len(data[agent]) > 0


class TestDimensionsEndpoint:
    """Dimensions endpoint tests"""
    
    def test_dimensions_returns_available_dimensions(self):
        """Test /api/dimensions returns available dimensions"""
        response = requests.get(f"{BASE_URL}/api/dimensions")
        assert response.status_code == 200
        data = response.json()
        
        assert "dimensions" in data
        dims = data["dimensions"]
        
        # Verify we have 3 dimension types
        assert len(dims) == 3
        
        # Verify dimension structure
        for dim in dims:
            assert "name" in dim
            assert "type" in dim
            assert "hierarchy" in dim


class TestChatEndpoint:
    """Chat endpoint tests - Natural language query processing"""
    
    def test_chat_processes_natural_language_query(self):
        """Test POST /api/chat processes natural language queries and returns analysis results"""
        payload = {
            "message": "Show Q4 sales by region"
        }
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=60  # LLM calls can take time
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "response" in data
        assert "session_id" in data
        assert "analysis_result" in data
        
        # Verify response is not empty
        assert len(data["response"]) > 0
        
        # Verify analysis_result has data
        if data["analysis_result"]:
            assert "data" in data["analysis_result"]
            assert "row_count" in data["analysis_result"]
            assert data["analysis_result"]["row_count"] > 0
    
    def test_chat_with_session_id(self):
        """Test chat maintains session context"""
        session_id = "test-session-123"
        payload = {
            "message": "What's the total sales by category?",
            "session_id": session_id
        }
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=60
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify session_id is returned
        assert data["session_id"] == session_id


class TestOLAPQueryEndpoint:
    """Direct OLAP query endpoint tests"""
    
    def test_olap_query_with_dimensions_and_measures(self):
        """Test POST /api/olap/query with custom dimensions and measures"""
        payload = {
            "operation": "aggregate",
            "dimensions": ["region", "quarter"],
            "measures": ["sales_amount", "quantity"],
            "filters": {}
        }
        response = requests.post(
            f"{BASE_URL}/api/olap/query",
            json=payload
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert "row_count" in data
        assert data["row_count"] > 0
    
    def test_olap_query_with_filters(self):
        """Test OLAP query with filters applied"""
        payload = {
            "operation": "slice",
            "dimensions": ["product"],
            "measures": ["sales_amount"],
            "filters": {"quarter": "Q4", "region": "North"}
        }
        response = requests.post(
            f"{BASE_URL}/api/olap/query",
            json=payload
        )
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert data["filters"]["quarter"] == "Q4"
        assert data["filters"]["region"] == "North"


class TestKPIEndpoint:
    """KPI summary endpoint tests"""
    
    def test_kpi_summary_returns_metrics(self):
        """Test /api/kpi/summary returns KPI metrics"""
        response = requests.get(f"{BASE_URL}/api/kpi/summary")
        assert response.status_code == 200
        data = response.json()
        
        # Verify KPI structure
        assert "total_revenue" in data
        assert "total_units_sold" in data
        assert "num_transactions" in data
        assert "average_order_value" in data
        assert "average_profit_margin" in data


class TestSalesByMonth:
    """Sales by month endpoint tests"""
    
    def test_sales_by_month_returns_monthly_data(self):
        """Test /api/olap/sales-by-month returns monthly breakdown"""
        response = requests.get(f"{BASE_URL}/api/olap/sales-by-month")
        assert response.status_code == 200
        data = response.json()
        
        assert "data" in data
        assert "row_count" in data
        assert data["row_count"] > 0
        
        # Verify month data structure
        for item in data["data"]:
            assert "month" in item
            assert "total_sales_amount" in item


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
