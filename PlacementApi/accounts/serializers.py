from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from course.models import CourseYearAllowed
from django.core.validators import RegexValidator


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
        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        user.is_active = False
        user.save()
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer): 
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['roll'] = user.username
        try:
            student = user.student
            token["first_name"] = student.first_name
            token["last_name"] = student.last_name
            token["img_url"] = "http://sakhanithnith.pagekite.me/" + student.image_url.url
            allowed_for = CourseYearAllowed.objects.get(year = student.current_year,course = student.course).type_allowed
            token["allowed_for"] = allowed_for
        except:
            pass


        return token
    # def validate(self, attrs):
    #     data =  super().validate(attrs)
    #     request = self.context["request"]
    #     image_url = request.build_absolute_uri(self.user.student.image_url.url)
    #     data["image_url"] = image_url
    #     return data
    