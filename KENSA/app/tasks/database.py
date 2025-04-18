import sqlite3
from contextlib import closing

# Global variable for the database connection
conn = None

def init_db():
    """
    Initializes the SQLite database and creates tables if they do not exist.
    """
    global conn
    conn = sqlite3.connect('crm.db')  # Creates a database file named 'crm.db' if not present
    
    with closing(conn.cursor()) as cursor:
        # Create Customers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create Tasks table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            priority INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    
    conn.commit()


def execute_query(query: str, params: tuple = ()) -> list:
    """
    Executes a SQL query and returns the result.
    
    Args:
        query (str): The SQL query to execute.
        params (tuple): Parameters to bind to the query.
    
    Returns:
        list: List of rows returned by the query.
    """
    global conn
    if conn is None:
        raise ConnectionError("Database connection is not initialized. Call `init_db` first.")
    
    with closing(conn.cursor()) as cursor:
        cursor.execute(query, params)
        conn.commit()
        return cursor.fetchall()


def close_db():
    """
    Closes the database connection.
    """
    global conn
    if conn:
        conn.close()
        conn = None


def insert_customer(customer_id: str, name: str, email: str, phone: str = None) -> None:
    """
    Inserts a new customer into the database.
    
    Args:
        customer_id (str): Unique identifier for the customer.
        name (str): Customer's name.
        email (str): Customer's email.
        phone (str): Customer's phone number.
    
    Returns:
        None
    """
    query = '''
    INSERT INTO customers (id, name, email, phone)
    VALUES (?, ?, ?, ?)
    '''
    execute_query(query, (customer_id, name, email, phone))


def get_customer(customer_id: str) -> dict:
    """
    Retrieves a customer's information by ID.
    
    Args:
        customer_id (str): Unique identifier for the customer.
    
    Returns:
        dict: Customer data if found, otherwise None.
    """
    query = 'SELECT * FROM customers WHERE id = ?'
    result = execute_query(query, (customer_id,))
    if result:
        return dict(zip(['id', 'name', 'email', 'phone', 'created_at'], result[0]))
    return None


def delete_customer(customer_id: str) -> None:
    """
    Deletes a customer by ID.
    
    Args:
        customer_id (str): Unique identifier for the customer.
    
    Returns:
        None
    """
    query = 'DELETE FROM customers WHERE id = ?'
    execute_query(query, (customer_id,))


def insert_task(task_id: str, description: str, priority: int, status: str = 'pending') -> None:
    """
    Inserts a new task into the database.
    
    Args:
        task_id (str): Unique identifier for the task.
        description (str): Task description.
        priority (int): Task priority (lower number = higher priority).
        status (str): Task status (e.g., 'pending', 'completed').
    
    Returns:
        None
    """
    query = '''
    INSERT INTO tasks (id, description, priority, status)
    VALUES (?, ?, ?, ?)
    '''
    execute_query(query, (task_id, description, priority, status))


def get_task(task_id: str) -> dict:
    """
    Retrieves a task's information by ID.
    
    Args:
        task_id (str): Unique identifier for the task.
    
    Returns:
        dict: Task data if found, otherwise None.
    """
    query = 'SELECT * FROM tasks WHERE id = ?'
    result = execute_query(query, (task_id,))
    if result:
        return dict(zip(['id', 'description', 'priority', 'status', 'created_at'], result[0]))
    return None


def delete_task(task_id: str) -> None:
    """
    Deletes a task by ID.
    
    Args:
        task_id (str): Unique identifier for the task.
    
    Returns:
        None
    """
    query = 'DELETE FROM tasks WHERE id = ?'
    execute_query(query, (task_id,))
