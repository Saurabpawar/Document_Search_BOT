import mysql.connector
from werkzeug.security import generate_password_hash

# Establish a connection to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Replace with your MySQL host if needed
        user="root",            # Replace with your MySQL username
        password="root",        # Replace with your MySQL password
        database="user_auth"    # Replace with your actual database name
    )

# Function to insert a new user into the database
def add_user_to_db(username, password, role):
    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # SQL query to insert user data
    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    values = (username, hashed_password, role)

    # Connect to the database and execute the query
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, values)
        connection.commit()  # Commit the transaction
        print(f"User '{username}' added successfully with role '{role}'!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

# Main function to get user input and add user
def main():
    # Get user input for username, password, and role
    username = input("Enter username: ")
    password = input("Enter password: ")
    role = input("Enter role (admin/user): ")

    # Validate role
    if role not in ["admin", "user"]:
        print("Invalid role! Please enter 'admin' or 'user'.")
        return

    # Call the function to add user to the database
    add_user_to_db(username, password, role)

if __name__ == "__main__":
    main()
