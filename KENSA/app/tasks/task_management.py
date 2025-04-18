import heapq

# In-memory priority queue and lookup for tasks
task_heap = []  # Stores (priority, task_id) for quick priority management
task_lookup = {}  # Maps task_id to task_data for fast retrieval and updates

def add_task(task_id: str, task_data: dict) -> None:
    """
    Adds a new task to the priority queue and task lookup.

    Args:
        task_id (str): Unique identifier for the task.
        task_data (dict): Data related to the task (e.g., description, priority, etc.).
            Must include a 'priority' key (higher priority = lower numerical value).

    Returns:
        None
    """
    if task_id in task_lookup:
        raise ValueError(f"Task with ID '{task_id}' already exists.")
    
    priority = task_data.get('priority', 0)  # Default priority is 0 if not provided
    heapq.heappush(task_heap, (priority, task_id))  # Add to priority queue
    task_lookup[task_id] = task_data  # Add to task lookup


def get_next_task() -> dict:
    """
    Retrieves and removes the highest-priority task from the queue.

    Returns:
        dict: The task data of the highest-priority task.
        None: If there are no tasks in the queue.
    """
    if not task_heap:
        return None

    _, task_id = heapq.heappop(task_heap)  # Get the highest-priority task
    return task_lookup.pop(task_id, None)  # Remove from task lookup and return


def update_task(task_id: str, updated_data: dict) -> None:
    """
    Updates the data of an existing task. If priority changes, re-heapifies the queue.

    Args:
        task_id (str): Unique identifier for the task.
        updated_data (dict): Dictionary containing updated task data.

    Returns:
        None
    """
    if task_id not in task_lookup:
        raise KeyError(f"Task with ID '{task_id}' not found.")

    # Update task data
    task_lookup[task_id].update(updated_data)

    # If priority is updated, re-heapify the queue
    if 'priority' in updated_data:
        # Remove and re-add the task to update its priority
        for i, (priority, t_id) in enumerate(task_heap):
            if t_id == task_id:
                del task_heap[i]
                heapq.heapify(task_heap)  # Restore heap structure after deletion
                break
        new_priority = updated_data['priority']
        heapq.heappush(task_heap, (new_priority, task_id))


def delete_task(task_id: str) -> None:
    """
    Deletes a task from the priority queue and lookup.

    Args:
        task_id (str): Unique identifier for the task.

    Returns:
        None
    """
    if task_id not in task_lookup:
        raise KeyError(f"Task with ID '{task_id}' not found.")

    # Remove the task from the heap
    for i, (_, t_id) in enumerate(task_heap):
        if t_id == task_id:
            del task_heap[i]
            heapq.heapify(task_heap)  # Restore heap structure after deletion
            break

    # Remove from lookup
    del task_lookup[task_id]


def get_all_tasks() -> list:
    """
    Retrieves all tasks currently in the queue.

    Returns:
        list: List of all task data dictionaries.
    """
    return list(task_lookup.values())


# Example Usage (comment out for production)
if __name__ == "__main__":
    # Add sample tasks
    add_task("task1", {"description": "Fix bug in system", "priority": 1})
    add_task("task2", {"description": "Write documentation", "priority": 3})
    add_task("task3", {"description": "Prepare presentation", "priority": 2})

    # View all tasks
    print("All Tasks:", get_all_tasks())

    # Get the next task
    print("Next Task:", get_next_task())

    # Update a task
    update_task("task3", {"priority": 0})
    print("All Tasks After Update:", get_all_tasks())

    # Delete a task
    delete_task("task2")
    print("All Tasks After Deletion:", get_all_tasks())
