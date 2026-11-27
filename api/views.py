from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from finance.models import Operation
from .serializers import OperationSerializer

# --- 1. CRUD для Операций ---
class OperationListCreateView(APIView):
    permission_classes = [IsAuthenticated] # Защита: только с токеном

    def get(self, request):
        operations = Operation.objects.filter(user=request.user)
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OperationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Возвращаем 422 при ошибке валидации (как в методичке)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OperationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Operation, pk=pk, user=user)

    def get(self, request, pk):
        operation = self.get_object(pk, request.user)
        serializer = OperationSerializer(operation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        operation = self.get_object(pk, request.user)
        operation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- 2. Админский эндпоинт (для проверки 403) ---
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] # Только для админов

    def get(self, request):
        return Response({"message": "Привет, Админ!"}, status=status.HTTP_200_OK)