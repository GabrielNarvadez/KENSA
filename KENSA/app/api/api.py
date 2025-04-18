from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.models import Customer, Task
from app.tasks.sentiment_analysis import analyze_sentiment

# Customer Endpoints
@api_view(['POST'])
def create_customer(request):
    data = request.data
    try:
        customer = Customer.objects.create(
            id=data['id'],
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', None)
        )
        return Response({"message": f"Customer {customer.name} created successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def retrieve_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        return Response({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "created_at": customer.created_at
        }, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_customer_endpoint(request, customer_id):
    data = request.data
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        customer.save()
        return Response({"message": "Customer updated successfully!"}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_customer_endpoint(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        return Response({"message": "Customer deleted successfully!"}, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

# Task Endpoints
@api_view(['POST'])
def create_task(request):
    data = request.data
    try:
        task = Task.objects.create(
            id=data['id'],
            description=data['description'],
            priority=data.get('priority', 0),
            status=data.get('status', 'pending')
        )
        return Response({"message": f"Task {task.description} created successfully!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_next_task_endpoint(request):
    try:
        task = Task.objects.filter(status='pending').order_by('priority').first()
        if task:
            return Response({
                "id": task.id,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "created_at": task.created_at
            }, status=status.HTTP_200_OK)
        return Response({"error": "No tasks available"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_all_tasks(request):
    tasks = Task.objects.all()
    task_list = [
        {
            "id": task.id,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "created_at": task.created_at
        }
        for task in tasks
    ]
    return Response(task_list, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_task_endpoint(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return Response({"message": "Task deleted successfully!"}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

# Sentiment Analysis Endpoint
@api_view(['POST'])
def analyze_feedback(request):
    feedback = request.data.get('feedback', '')
    if not feedback:
        return Response({"error": "Feedback text is required"}, status=status.HTTP_400_BAD_REQUEST)
    sentiment = analyze_sentiment(feedback)
    return Response(sentiment, status=status.HTTP_200_OK)
