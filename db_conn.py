import os 
import psycopg2  
from psycopg2.extras import RealDictCursor  # It is used to return query results as dictionaries rather than tuples. 
from dotenv import load_dotenv

load_dotenv('.env')

class Postgresql:
    def __init__(self):
        self.conn = None
        self.cursor = None 
    
        self.host = "localhost"
        self.database = "splitpay"
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.port = 5432
        
    def create_connection(self):
       """Establishes a connection to the PostgreSQL database."""
       try:
        print("Establishing the Postgresql connection...")
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
            cursor_factory=RealDictCursor
        )
        # print(self.conn)
        
        if self.conn:
            print("Connection established successfully")
            return self.conn 
       except Exception as e:
            print(f"Error while connecting to DB: {e}")
    
    def execute_query(self, query, params=None, fetch=True):
        """Executes a SQL query. If fetch is True, returns data; otherwise, commits changes."""
        results = []
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if fetch:
                    results = cursor.fetchall()
                else:
                    self.conn.commit()
                    print("Query executed successfully")

        except Exception as e:
            print(f"Error while executing query: {e}")
            self.conn.rollback()

        return results

    def close_connection(self):
        """Closes the connection to the database."""
        if self.conn:
            self.conn.close()
            self.conn = None


# if __name__ == "__main__":
#     db = Postgresql()
#     db.create_connection()
#     print(db.execute_query('select * from users'))
#     db.close_connection()