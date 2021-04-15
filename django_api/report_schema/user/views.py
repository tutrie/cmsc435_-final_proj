from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='create_user', url_name='create_user')
    def create_user(self, request):
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            print(serialized.initial_data)
            User.objects.create_user(
                serialized.initial_data['username'],
                serialized.initial_data['email'],
                serialized.initial_data['password']
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
