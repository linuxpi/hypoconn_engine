import secrets

from rest_framework import (
    views as rest_views,
    response as rest_responses,
    permissions as rest_permissions,
    serializers as rest_serializers
)

from .models import UserToken
from .utils import scrape_api_token
from . import TOKEN_LENGTH

class LoginSerializer(rest_serializers.ModelSerializer):

    password = rest_serializers.CharField(write_only=True)
    token = rest_serializers.CharField(read_only=True)

    class Meta:
        model = UserToken
        fields = ('username', 'password', 'token')

    def validate(self, attrs):
        attrs = super(LoginSerializer, self).validate(attrs=attrs)
        try:
            self.instance = UserToken.objects.get(username=attrs['username'])
            # update token when login
        except UserToken.DoesNotExist:
            attrs['token'] = secrets.token_hex(TOKEN_LENGTH)
        attrs['api_token'] = scrape_api_token(attrs['username'], attrs['password'])
        attrs.pop('password')
        return attrs


class LoginView(rest_views.APIView):

    permission_classes = [rest_permissions.AllowAny]
    serializer_class = LoginSerializer

    # Create permission for expired token error while fetching data
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        print(serializer.instance.api_token)
        return rest_responses.Response({
            'token': serializer.instance.token
        })
