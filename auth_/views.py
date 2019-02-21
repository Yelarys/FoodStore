from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import authentication
from rest_framework import status
from main.serializers import UserModelSerializer
from django.contrib.auth.models import User


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authentication.authenticate(username=username, password=password)
    if user is None:
        return Response({'user': user}, status=status.HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)
    context = {
        'key': token.key,
    }
    return Response(context)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    request.user.auth_token.delete()
    return Response({'detail': 'Succesfully loged out'})


@api_view(['POST'])
def register(request):
    serializer = UserModelSerializer(data=request.data)
    if serializer.is_valid():
        User.objects.create_user(
            request.data.get('username'),
            request.data.get('email'),
            request.data.get('password')
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)