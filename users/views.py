from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse, HttpResponsePermanentRedirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils import Util
from .models import User
from .permissions import IsOwnerOrReadOnly
from .serializers import EmailVerificationSerializer, RegistrationSerializer, ResetPasswordEmailRequestSerializer, \
    SetNewPasswordSerializer, LoginSerializer, UserSerializer


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import os
import jwt


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.headers['Authorization']
        print(token)
        if 'Bearer' in token:
            token = token.split()[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            print(payload)
            if 'user_id' in payload:
                user = User.objects.get(id=payload['user_id'])
            else:
                user = User.objects.get(id=payload['id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        abs_url = 'http://lk.norma.kg/auth/activate/' + str(token)
        email_body = 'hello' + user.first_name + \
                     'Use this link to activate your email\n ' \
                     'The link will be active for 10 minutes \n' + \
                     abs_url
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        Util.send_email(data)   
        return Response(user_data, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     email = request.data.get('email', '')
    #
    #     if User.objects.filter(email=email).exists():
    #         user = User.objects.get(email=email)
    #         uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    #         token = PasswordResetTokenGenerator().make_token(user)
    #         # relativeLink = reverse('users:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
    #
    #         redirect_url = request.data.get('redirect_url', '')
    #         abs_url = f'http://lk.norma.kg/newpassword/?uid={uidb64}&token={token}'
    #
    #         email_body = 'Hello, \n Use link below to reset your password  \n' + \
    #                      abs_url + "?redirect_url=" + redirect_url
    #         data = {'email_body': email_body, 'to_email': user.email,
    #                 'email_subject': 'Reset your password'}
    #         Util.send_email(data)
    #         response_data = [
    #             {
    #                 'token': token,
    #                 'uidb64': uidb64
    #             },
    #             {
    #                 'success': 'We have sent you a link to reset your password'
    #             }
    #         ]
    #         return Response(response_data, status=status.HTTP_200_OK)
    #     return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class RequestPasswordResetEmailAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    queryset = User.objects.all()

    def post(self, request):
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # relativeLink = reverse('users:password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            abs_url = f'http://lk.norma.kg/newpassword/?uid={uidb64}&token={token}'

            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                         abs_url + "?redirect_url=" + redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}
            Util.send_email(data)
            response_data = [
                {
                    'token': token,
                    'uidb64': uidb64
                },
                {
                    'success': 'We have sent you a link to reset your password'
                }
            ]
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckGenericAPIView(generics.GenericAPIView):
    # serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url + '?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                user.is_active = True
                return CustomRedirect(
                    redirect_url + '?token_valid=True&message=Credentials Valid&uidb64=' + uidb64 + '&token=' + token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '') + '?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url + '?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'},
                                status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        users = self.queryset.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        try:
            serializer = self.serializer_class(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse({'status': 0, 'message': 'Error on user update'})

    def list(self, request):
        queryset = User.objects.all()
        return Response(queryset)


class CurrentUserView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ('email', )
