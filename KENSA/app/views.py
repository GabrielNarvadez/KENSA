from django.shortcuts import render 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json

from django.shortcuts import render, redirect, get_object_or_404
from app.models import Customer, Task
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json

from app.models import Customer, Task
from django.shortcuts import render, redirect
from .models import Task
import heapq



# Add these global variables
undo_stack = []
redo_stack = []


def index(request):
    sync_customer_db()  # Ensure the in-memory data is up-to-date
    query = request.GET.get('q', '').strip()  # Get query string from the URL

    if query:
        # Perform case-insensitive partial match search using in-memory data
        customers = [data for data in customer_db.values() if matches_query(data, query)]
    else:
        # Fetch all customers if no query is provided
        customers = list(customer_db.values())


    # Render the template with the filtered or full list of customers
    return render(request, 'app/index.html', {'customers': customers})



def tasks(request):
    if request.method == 'POST':
        if 'delete_task' in request.POST:
            # Handle task deletion
            task_id = request.POST.get('delete_task')
            Task.objects.filter(id=task_id).delete()
            return redirect('tasks')

        elif 'task_id' in request.POST:
            # Handle updates
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)

            # Update priority if provided
            if 'priority' in request.POST and request.POST['priority']:
                task.priority = int(request.POST['priority'])

            # Update is_completed status
            task.is_completed = 'is_completed' in request.POST

            # Save the task
            task.save()
            return redirect('tasks')

        elif 'task_name' in request.POST:
            # Add new task
            task_name = request.POST.get('task_name')
            priority = request.POST.get('priority', 1)  # Default priority to 1 if not provided
            is_completed = 'is_completed' in request.POST
            Task.objects.create(task_name=task_name, priority=int(priority), is_completed=is_completed)
            return redirect('tasks')

    # Sorting logic with a heap
    all_tasks = list(Task.objects.all())
    heap = []
    sort_order = request.GET.get('sort', 'asc')

    if sort_order == 'desc':
        # Max-heap for descending order
        for task in all_tasks:
            heapq.heappush(heap, (-task.priority, task.id))  # Store task ID as a reference
        sorted_task_ids = [heapq.heappop(heap)[1] for _ in range(len(heap))]
    else:
        # Min-heap for ascending order
        for task in all_tasks:
            heapq.heappush(heap, (task.priority, task.id))  # Store task ID as a reference
        sorted_task_ids = [heapq.heappop(heap)[1] for _ in range(len(heap))]

    # Retrieve sorted tasks based on IDs
    tasks_list = [Task.objects.get(id=task_id) for task_id in sorted_task_ids]

    return render(request, 'app/tasks.html', {
        'tasks': tasks_list,
        'sort_order': sort_order
    })

def invoice(request): 
    return render(request, 'app/invoice.html') 
# In-memory dictionary to cache customer data
customer_db = {}



def sync_customer_db():
    """Synchronize in-memory data with the database."""
    global customer_db
    customer_db = {
        customer.id: {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "item_name": customer.item_name,
            "amount": customer.amount,
            "customer_comments": customer.customer_comments,
            "status": customer.status,
            "ai_analysis": customer.ai_analysis,
        }
        for customer in Customer.objects.all()
    }

def matches_query(data: dict, query) -> bool:
    if isinstance(query, str):  # Handle string queries
        query = query.lower()
        return (
            query in (data.get('name', '') or '').lower() or
            query in (data.get('email', '') or '').lower() or
            query in (data.get('phone', '') or '').lower() or
            query in (data.get('item_name', '') or '').lower()
        )
    elif isinstance(query, dict):  # Handle dictionary queries
        return all((data.get(key, '') or '').lower() == value.lower() for key, value in query.items())
    return False  # Default to no match for unsupported query types






def search_customers_view(request):
    if request.method == "GET":
        sync_customer_db()  # Ensure in-memory data is up-to-date
        query = request.GET.get('q', '').strip()  # Get the search query
        if query:
            # Case-insensitive partial matching
            results = [data for data in customer_db.values() if matches_query(data, query)]
        else:
            results = list(customer_db.values())  # Fetch all if no query provided
        return render(request, 'app/index.html', {'customers': results})
    else:
        return redirect('/')

@csrf_exempt
def add_customer_view(request):
    if request.method == "POST":
        try:
            # Ensure required fields exist
            customer_id = request.POST.get('id', '').strip()
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()

            if not customer_id or not name or not email:
                raise ValueError("ID, Name, and Email are required.")

            if Customer.objects.filter(id=customer_id).exists():
                raise ValueError(f"Customer with ID '{customer_id}' already exists.")

            # Collect optional fields
            phone = request.POST.get('phone', '').strip()
            item_name = request.POST.get('item_name', '').strip()
            amount = request.POST.get('amount', None)
            customer_comments = request.POST.get('customer_comments', '').strip()
            status = request.POST.get('status', 'pending')
            ai_analysis = request.POST.get('ai_analysis', None)

            # Create the new customer
            customer = Customer.objects.create(
                id=customer_id,
                name=name,
                email=email,
                phone=phone,
                item_name=item_name,
                amount=amount,
                customer_comments=customer_comments,
                status=status,
                ai_analysis=ai_analysis,
            )

            # Log the action for undo
            undo_stack.append({'action': 'delete', 'data': customer.id})
            redo_stack.clear()  # Clear redo stack after a new action

            # Update in-memory cache
            sync_customer_db()

            return redirect('/')
        except Exception as e:
            return render(request, 'app/index.html', {'error': str(e), 'customers': customer_db.values()})

    return render(request, 'app/index.html', {'customers': customer_db.values()})

@csrf_protect
def update_customer_view(request):
    if request.method == "POST":
        try:
            customer_id = request.POST.get('id')
            customer = get_object_or_404(Customer, id=customer_id)
            
            # Backup current state for undo
            old_data = {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "item_name": customer.item_name,
                "amount": customer.amount,
                "customer_comments": customer.customer_comments,
                "status": customer.status,
                "ai_analysis": customer.ai_analysis,
            }
            undo_stack.append({'action': 'update', 'data': old_data})
            redo_stack.clear()  # Clear redo stack after a new action
            
            # Update fields
            customer.name = request.POST.get('name', customer.name)
            customer.email = request.POST.get('email', customer.email)
            customer.phone = request.POST.get('phone', customer.phone)
            customer.item_name = request.POST.get('item_name', customer.item_name)
            
            amount = request.POST.get('amount')
            if amount:
                customer.amount = float(amount)
            
            customer.customer_comments = request.POST.get('customer_comments', customer.customer_comments)
            customer.status = request.POST.get('status', customer.status)
            customer.ai_analysis = request.POST.get('ai_analysis', customer.ai_analysis)
            customer.save()

            # Update in-memory cache
            sync_customer_db()

            return redirect('/')
        except Exception as e:
            return render(request, 'app/index.html', {'error': str(e), 'customers': customer_db.values()})
    else:
        return redirect('/')


@csrf_exempt
def delete_customer_view(request):
    if request.method == "POST":
        try:
            customer_id = request.POST.get('id')
            customer = get_object_or_404(Customer, id=customer_id)
            
            # Backup current state for undo
            old_data = {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone,
                "item_name": customer.item_name,
                "amount": customer.amount,
                "customer_comments": customer.customer_comments,
                "status": customer.status,
                "ai_analysis": customer.ai_analysis,
            }
            undo_stack.append({'action': 'create', 'data': old_data})
            redo_stack.clear()  # Clear redo stack after a new action
            
            # Delete the customer
            customer.delete()

            # Update in-memory cache
            sync_customer_db()

            return redirect('/')
        except Exception as e:
            return render(request, 'app/index.html', {'error': str(e), 'customers': customer_db.values()})
    else:
        return redirect('/')

def undo_view(request):
    if request.method == "POST":
        try:
            if not undo_stack:
                return JsonResponse({'status': 'error', 'message': 'No actions to undo.'}, status=400)
            
            action = undo_stack.pop()
            
            # Prepare the inverse action for redo
            if action['action'] == 'create':  # Undoing a "create" means deleting the item
                redo_stack.append({'action': 'delete', 'data': action['data']['id']})
                Customer.objects.filter(id=action['data']['id']).delete()
            elif action['action'] == 'delete':  # Undoing a "delete" means recreating the item
                redo_stack.append({'action': 'create', 'data': action['data']})
                Customer.objects.create(**action['data'])
            elif action['action'] == 'update':  # Undoing an "update" reverts to old data
                current_data = Customer.objects.filter(id=action['data']['id']).values().first()
                redo_stack.append({'action': 'update', 'data': current_data})
                Customer.objects.filter(id=action['data']['id']).update(**action['data'])

            sync_customer_db()
            return JsonResponse({'status': 'success', 'message': 'Undo successful.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def redo_view(request):
    if request.method == "POST":
        try:
            if not redo_stack:
                return JsonResponse({'status': 'error', 'message': 'No actions to redo.'}, status=400)
            
            action = redo_stack.pop()
            
            # Reapply the action and prepare its inverse for undo
            if action['action'] == 'create':  # Redoing "create" means recreating the item
                undo_stack.append({'action': 'delete', 'data': action['data']['id']})
                Customer.objects.create(**action['data'])
            elif action['action'] == 'delete':  # Redoing "delete" means deleting the item
                undo_stack.append({'action': 'create', 'data': action['data']})
                Customer.objects.filter(id=action['data']).delete()
            elif action['action'] == 'update':  # Redoing "update" means applying new data
                current_data = Customer.objects.filter(id=action['data']['id']).values().first()
                undo_stack.append({'action': 'update', 'data': current_data})
                Customer.objects.filter(id=action['data']['id']).update(**action['data'])

            sync_customer_db()
            return JsonResponse({'status': 'success', 'message': 'Redo successful.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

# Initialize in-memory database on startup
sync_customer_db()