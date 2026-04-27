from werkzeug.security import generate_password_hash, check_password_hash
from db_conn import Postgresql 

class Authentication:
    
    def __init__(self):
        self.db = Postgresql()
        self.db.create_connection()

    def check_user_exists(self, email):
        query = "SELECT email FROM users WHERE email = %s" 
        results = self.db.execute_query(query, (email,), fetch=True)

        return len(results) > 0 if results else False

    def register_user(self, username, email, password):

        if self.check_user_exists(email):
            return {
                "SUCCESS": False,
                "MESSAGE": "User already exists"
            }
        password_hash = generate_password_hash(password)
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"

        try:
            self.db.execute_query(query, (username, email, password_hash), fetch=False)
            return {
                "SUCCESS": True,
                "MESSAGE": "User registered successfully"
            }
        except Exception as e:
            return {
                "SUCCESS": False,
                "MESSAGE": f"Failed to register user: {e}"
            }

    def login_user(self, email, password):
        query = "SELECT username, email, password from users where email = %s"
        
        results = self.db.execute_query(query, (email,), fetch=True)

        if not results:
            return {
                "SUCCESS": False,
                "MESSAGE": "User not found"
            }
        
        user = results[0]

        if not check_password_hash(user["password"], password):
            return {
                "SUCCESS": False,
                "MESSAGE": "Invalid password"
            }

        return {
            "SUCCESS": True,
            "user": {
                "username": user["username"],
                "email": user["email"]
            }
        }