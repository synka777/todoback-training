from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Task
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Create a new task
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def task_create(request):
    data = request.data  # Using DRF's request.data to handle the incoming JSON data

    new_task = Task.objects.create( # Use the model's built-in objects.create() function to store an instance of said object in DB
        title=data["title"],
        completed=data.get("completed", False)  # Use `.get()` to provide a default value
    )
    return Response({ # We use Response instead of JsonResponse() because we're using DRF
        "id": new_task.id,
        "title": new_task.title,
        "completed": new_task.completed
    }, status=201)


# List all tasks
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_list(request):
    if request.method == "GET":
        # tasks = list(Task.objects.values())  # Get all tasks as a list of dictionaries
        tasks = Task.objects.all()

        # Get the 'completed' query param
        completed_param = request.GET.get("completed")

        if completed_param is not None:
            if completed_param.lower() == "true":
                tasks = tasks.filter(completed=True)
            elif completed_param.lower() == "false":
                tasks = tasks.filter(completed=False)

        return Response(tasks.values())  # DRF's Response is used here instead of JsonResponse


# Get a single task by ID
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    # Just use get_object_or_404() when a query parameter is passed in the URL
    task = get_object_or_404(Task, pk=pk)
    return Response({
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    })


# Update a task
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = request.data

    # Get the new values for each attribute, use the old ones if no new value provided
    task.title = data.get("title", task.title)
    task.completed = data.get("completed", task.completed)
    task.save() # Then save the updated task

    return Response({
        "id": task.id,
        "title": task.title,
        "completed": task.completed
    })


# Delete a task
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return Response({
        "message": "Deletion successful"
    }, status=204)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    # Check if the given user already exists
    if User.objects.filter(username=username).exists(): # The status code below could just be "400" instead but it's less explicit
        return Response({"detail": "Username is already taken"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the new user
    user = User.objects.create_user(username=username, password=password)

    # Create and return the token
    token, created = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=status.HTTP_201_CREATED)


# Login (authenticate and get token)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    data = request.data

    user = authenticate(username=data["username"], password=data["password"])
    if user:
        # Create or retrieve the user's token
        token, created = Token.objects.get_or_create(user=user) # Get the token by destructuring
        return Response({"token": token.key})  # Return the token in the response
    return Response({"detail": "Invalid credentials"}, status=401)
