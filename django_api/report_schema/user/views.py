from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited.

    Inherits from the predefined model viewset.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='create_user', url_name='create_user')
    def create_user(self, request: Request) -> Response:
        """Endpoint that accepts a POST request to create a new user in the database. No authentication is neccessary.

        Args:
            request (Request): Request body should be a json object in the form of:
            {
                username: <string>,
                password: <string>,
                email: <string>
            }

        Returns:
            Response: Returns a Response object with a status code and a json body in the form of:
            {
                username: <string>,
                email: <string>
            }
        """
        serialized_request_data = UserSerializer(data=request.data)
        if serialized_request_data.is_valid():
            # Create user from initial data because using the UserSerializer hides the password
            User.objects.create_user(
                serialized_request_data.initial_data['username'],
                serialized_request_data.initial_data['email'],
                serialized_request_data.initial_data['password']
            )
            return Response(serialized_request_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_request_data._errors, status=status.HTTP_400_BAD_REQUEST)
