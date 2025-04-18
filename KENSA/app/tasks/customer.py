# customer.py
# Module to manage customer data using dictionaries for CRUD operations.

# In-memory dictionary to store customer data
customer_db = {}

def add_customer(customer_id: str, customer_data: dict) -> None:
    """
    Adds a new customer to the database.
    
    Args:
        customer_id (str): Unique identifier for the customer.
        customer_data (dict): Data related to the customer (e.g., name, email, etc.).
    
    Returns:
        None
    """
    if customer_id in customer_db:
        raise ValueError(f"Customer with ID '{customer_id}' already exists.")
    customer_db[customer_id] = customer_data


def get_customer(customer_id: str) -> dict:
    """
    Retrieves a customer's data by ID.
    
    Args:
        customer_id (str): Unique identifier for the customer.
    
    Returns:
        dict: Customer data if found, otherwise None.
    """
    return customer_db.get(customer_id)


def update_customer(customer_id: str, updated_data: dict) -> None:
    """
    Updates an existing customer's data.
    
    Args:
        customer_id (str): Unique identifier for the customer.
        updated_data (dict): Dictionary containing updated data for the customer.
    
    Returns:
        None
    """
    if customer_id not in customer_db:
        raise KeyError(f"Customer with ID '{customer_id}' not found.")
    customer_db[customer_id].update(updated_data)


def delete_customer(customer_id: str) -> None:
    """
    Deletes a customer from the database by ID.
    
    Args:
        customer_id (str): Unique identifier for the customer.
    
    Returns:
        None
    """
    if customer_id not in customer_db:
        raise KeyError(f"Customer with ID '{customer_id}' not found.")
    del customer_db[customer_id]


def search_customers(query: dict) -> list:
    """
    Searches for customers that match the provided query parameters.
    
    Args:
        query (dict): Dictionary of key-value pairs to match against customer data.
    
    Returns:
        list: List of customer data dictionaries that match the query.
    """
    return [data for data in customer_db.values() if matches_query(data, query)]


def matches_query(data: dict, query: dict) -> bool:
    """
    Helper function to check if a customer's data matches the query parameters.
    
    Args:
        data (dict): Customer data dictionary.
        query (dict): Dictionary of key-value pairs to match against the data.
    
    Returns:
        bool: True if all query parameters match the data, False otherwise.
    """
    return all(data.get(key) == value for key, value in query.items())


# Example usage (remove or comment out before using in production)
if __name__ == "__main__":
    # Add some sample customers
    add_customer("1", {"name": "Alice", "email": "alice@example.com"})
    add_customer("2", {"name": "Bob", "email": "bob@example.com"})
    
    # Retrieve a customer
    print(get_customer("1"))  # Output: {'name': 'Alice', 'email': 'alice@example.com'}
    
    # Update a customer
    update_customer("1", {"phone": "123-456-7890"})
    print(get_customer("1"))  # Output: {'name': 'Alice', 'email': 'alice@example.com', 'phone': '123-456-7890'}
    
    # Search for customers
    print(search_customers({"email": "bob@example.com"}))  # Output: [{'name': 'Bob', 'email': 'bob@example.com'}]
    
    # Delete a customer
    delete_customer("2")
    print(get_customer("2"))  # Output: None
