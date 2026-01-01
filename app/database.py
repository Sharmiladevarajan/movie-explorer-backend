import psycopg2
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from app.config import settings
from app.utils.logger import logger


class DatabaseConnectionPool:
    """Database connection pool manager"""
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnectionPool, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        """Initialize connection pool"""
        if self._pool is None:
            try:
                # Test connection first before creating pool
                test_conn = psycopg2.connect(
                    host=settings.DB_HOST,
                    database=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    port=int(settings.DB_PORT)
                )
                test_conn.close()
                logger.info("Database connection test successful")
                
                # Create connection pool
                self._pool = psycopg2.pool.ThreadedConnectionPool(
                    settings.DB_MIN_CONN,
                    settings.DB_MAX_CONN,
                    host=settings.DB_HOST,
                    database=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    port=int(settings.DB_PORT)
                )
                logger.info(f"Database connection pool created (min={settings.DB_MIN_CONN}, max={settings.DB_MAX_CONN})")
            except Exception as e:
                logger.error(f"Failed to create connection pool: {str(e)}")
                raise

    def get_connection(self):
        """Get connection from pool"""
        if self._pool is None:
            self.initialize()
        try:
            return self._pool.getconn()
        except Exception as e:
            logger.error(f"Failed to get connection from pool: {str(e)}")
            raise

    def return_connection(self, conn):
        """Return connection to pool"""
        if self._pool and conn:
            self._pool.putconn(conn)

    def close_all(self):
        """Close all connections in pool"""
        if self._pool:
            self._pool.closeall()
            logger.info("All database connections closed")


# Global connection pool instance
db_pool = DatabaseConnectionPool()


class Database:
    """Database operations class with common query methods"""

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = db_pool.get_connection()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            if conn:
                db_pool.return_connection(conn)

    def execute_query(self, query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = True) -> Optional[Any]:
        """
        Execute a query with proper error handling
        
        Args:
            query: SQL query string
            params: Query parameters tuple
            fetch_one: Return single row
            fetch_all: Return all rows
        
        Returns:
            Query results or None
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                cursor.execute(query, params or ())
                
                if fetch_one:
                    return cursor.fetchone()
                elif fetch_all:
                    return cursor.fetchall()
                return None
        except psycopg2.Error as e:
            logger.error(f"Query execution error: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in execute_query: {str(e)}")
            raise

    def execute_insert(self, query: str, params: tuple) -> Optional[Dict]:
        """Execute INSERT query and return inserted row"""
        return self.execute_query(query, params, fetch_one=True)

    def execute_update(self, query: str, params: tuple) -> Optional[Dict]:
        """Execute UPDATE query and return updated row"""
        return self.execute_query(query, params, fetch_one=True)

    def execute_delete(self, query: str, params: tuple) -> bool:
        """Execute DELETE query and return success status"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Delete operation error: {str(e)}")
            raise

    def get_or_create(self, table: str, field: str, value: str, return_field: str = "id") -> Any:
        """
        Get existing record or create new one
        
        Args:
            table: Table name
            field: Field to search/insert
            value: Value to search/insert
            return_field: Field to return
        
        Returns:
            Value of return_field
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(cursor_factory=RealDictCursor)
                
                # Try to get existing
                select_query = sql.SQL("SELECT {return_field} FROM {table} WHERE {field} = %s").format(
                    return_field=sql.Identifier(return_field),
                    table=sql.Identifier(table),
                    field=sql.Identifier(field)
                )
                cursor.execute(select_query, (value,))
                result = cursor.fetchone()
                
                if result:
                    return result[return_field]
                
                # Create new
                insert_query = sql.SQL("INSERT INTO {table} ({field}) VALUES (%s) RETURNING {return_field}").format(
                    table=sql.Identifier(table),
                    field=sql.Identifier(field),
                    return_field=sql.Identifier(return_field)
                )
                cursor.execute(insert_query, (value,))
                result = cursor.fetchone()
                return result[return_field]
                
        except Exception as e:
            logger.error(f"get_or_create error for table {table}: {str(e)}")
            raise


# Global database instance
db = Database()
