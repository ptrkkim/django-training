from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from src.mailing.email_sending import notify_new_password_for_user
from src.core_auth.models import User
from src.core_auth.serializers import ChangePasswordSerializer, UserSerializer, RequestPasswordChangeSerializer


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        user.auth_token.delete()
        return Response()


class ChangePasswordViewTests(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['password_1'])
        request.user.save()
        return Response()


class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self, *args, **kwargs):
        return self.request.user


class PasswordResetView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RequestPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data.get('user')
        if user:
            new_password = User.objects.make_random_password()
            user.force_new_password(new_password)
            user.save()
            notify_new_password_for_user(user, new_password)

        return Response()


def admin_login_redirect_view(request):
    redirect_url = '/'
    if request.user.is_staff:
        redirect_url = reverse('admin:survey_survey_changelist')
    return redirect(redirect_url)


def admin_login(*args, **kwargs):
    kwargs['extra_context'] = {REDIRECT_FIELD_NAME: reverse(settings.LOGIN_REDIRECT_URL)}
    return admin.site.login(*args, **kwargs)
