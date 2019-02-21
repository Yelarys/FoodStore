from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import authenticate, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from .models import Order, Restaurant
from .serializers import UserModelSerializer, OrderModelSerializer, RestaurantModelSerializer
from django.contrib.auth.models import User
from django.http import Http404


@api_view(['GET'])
def order_list(request):
    queryset = Order.objects.all()
    serializer = OrderModelSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def restaurant_list(request):
    queryset = Restaurant.objects.all()
    serializer = RestaurantModelSerializer(queryset, many=True)
    return Response(serializer.data)


class OrderView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderModelSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer_info = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            return Http404

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderModelSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = Order.objects.get(id=pk)
        serializer = OrderModelSerializer(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = Order.objects.get(id=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RestaurantView(APIView):
    def get(self, request):
        rests = Restaurant.objects.all()
        serializer = RestaurantModelSerializer(rests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class RestaurantDetailView(APIView):
    def get_object(self, pk):
        try:
            return Restaurant.objects.get(id=pk)
        except Restaurant.DoesNotExist:
            return Http404

    def get(self, request, pk):
        rest = Restaurant.objects.get(id=pk)
        serializer = OrderModelSerializer(rest)
        return Response(serializer.data)

    def put(self, request, pk):
        rest = Restaurant.objects.get(id=pk)
        serializer = RestaurantModelSerializer(instance=rest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rest = Restaurant.objects.get(id=pk)
        rest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer


class OrderCreate(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = (IsAuthenticated,)

class OrderDetails(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer


class OrDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Order.objects.get(id=self.kwargs['pk'])


class RestaurantList(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantModelSerializer


class RestaurantDetails(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantModelSerializer


class RestaurantCreate(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantModelSerializer
    permission_classes = (IsAdminUser,)


class ResDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantModelSerializer
    permission_classes = (IsAdminUser,)

    def get_object(self):
        return Restaurant.objects.get(id=self.kwargs['pk'])


@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def register(request):
    serialized = UserModelSerializer(data=request.data)
    if serialized.is_valid():
        User.objects.create_user(
            request.data.get('username'),
            request.data.get('email'),
            request.data.get('password')
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
