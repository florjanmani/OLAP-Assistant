"""
Database module for OLAP Assistant.
Uses DuckDB with a Star Schema design for OLAP analytics.
"""

from .duckdb_manager import DuckDBManager, db_manager

__all__ = ['DuckDBManager', 'db_manager']
