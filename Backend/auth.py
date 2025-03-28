import mysql.connector
from flask import session
from werkzeug.security import check_password_hash  

def get_db_connection():
    """Establish a connection to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",      
        user="root",         
        password="root",     
        database="user_auth"  
    )

def authenticate():
    """Check if the user is authenticated and has a valid role stored in the session."""
    if 'username' in session and 'role' in session:
        return session['role']
    return None

def login(username, password):
    """Authenticate the user by checking the username and password against the database."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Query the database to find the user
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()  # Fetch the first matching record

        if user and check_password_hash(user['password'], password):  # Check password hash
            session['username'] = user['username']
            session['role'] = user['role']
            cursor.close()
            connection.close()
            return {"message": "Login successful", "role": user['role']}
        else:
            cursor.close()
            connection.close()
            return {"error": "Invalid credentials"}

    except mysql.connector.Error as err:
        cursor.close()
        connection.close()
        return {"error": f"Database error: {err}"}

def logout():
    """Logout the user by clearing the session."""
    session.clear()
    return {"message": "Logged out successfully"}
