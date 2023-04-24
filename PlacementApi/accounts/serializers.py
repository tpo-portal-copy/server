from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from course.models import CourseYearAllowed
from django.core.validators import RegexValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all()),RegexValidator(regex=r'\w+@nith\.ac\.in$')])

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','password2')
        extra_kwargs = {'password': {'write_only': True}}
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
    
        if not attrs['username'].isalnum():
            raise serializers.ValidationError('The username should contain only alphanumeric character')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.isActive = False
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer): 
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['roll'] = user.username
        print('token ----- ')
        try:
            student = user.student
            token["first_name"] = student.first_name
            token["last_name"] = student.last_name
            allowed_for = CourseYearAllowed.objects.get(year = student.current_year,course = student.course).type_allowed
            token["allowed_for"] = allowed_for
            token["img_url"] = "https://tpoportal.pagekite.me/" + student.image_url.url
        except:
            if user.username == "tpo@nith.ac.in":
                token["role"] = 'TPO'

        try:
            tpr = user.student_tpr
            print("This is TPR", tpr)
            token["role"] = 'TPR'
        except:
            print("Here it is")
            pass

        return token


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # email = serializers.EmailField(validators=[RegexValidator(regex=r'\w+@nith\.ac\.in$')])
    # redirect_url = serializers.CharField(max_length=500, required=False)

    def validate_email(self, email):
        email = email.lower().strip()
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email address does not exist.")
        return email


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, min_length=6, max_length=68, write_only=True, required=False)
    password2 = serializers.CharField(style={'input_type': 'password'}, min_length=6, max_length=68, write_only=True, required=False)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'password2', 'token', 'uidb64']

    def validate(self, attrs):
        user = None
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise exceptions.AuthenticationFailed('The reset link is invalid', 401)

        except Exception as e:
            raise exceptions.AuthenticationFailed('The reset link is invalid', 401)

        try:
            password = attrs["password"]
            password2 = attrs["password2"]

            if(password != password2):
                raise exceptions.ValidationError("The password and confirm password didn't match")
        except:
            pass
        # return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        uidb64 = validated_data["uidb64"]
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        print(user)
        user.set_password(validated_data["password"])
        user.save()
        return {"msg":"password reset successfully"}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)