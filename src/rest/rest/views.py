# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from .mongo_client import MongoDBClient

class TodoService:
    def __init__(self, db_client, collection_name):
        self.db_client = db_client
        self.collection_name = collection_name

    def get_all_todos(self):
        return self.db_client.find_all(self.collection_name, {'_id': 0})

    def add_todo(self, todo):
        self.db_client.insert_one(self.collection_name, todo)
        return self.get_all_todos()

    def delete_all_todos(self):
        result = self.db_client.delete_many(self.collection_name, {})
        return result.deleted_count

class TodoListView(APIView):
    parser_classes = [JSONParser]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todo_service = TodoService(MongoDBClient('test_db'), 'todos')

    def get(self, request):
        todos = self.todo_service.get_all_todos()
        return Response(todos, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            if 'title' not in data or not isinstance(data['title'], str) or not data['title'].strip():
                return Response({'error': 'Invalid title'}, status=status.HTTP_400_BAD_REQUEST)

            todo = {
                'title': data['title'].strip(),
            }

            todos = self.todo_service.add_todo(todo)
            return Response(todos, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            deleted_count = self.todo_service.delete_all_todos()
            return Response({'message': f'{deleted_count} todos deleted.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
