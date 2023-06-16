# from django.core.exceptions import ValidationError

from rest_framework import serializers
class Validate_file_size(serializers.Serializer):
    def __init__(self, limit, unit):
        self.limit = limit
        self.unit = unit

    def __call__(self, value):
        filesize = value.size
        if self.unit == "MB":
            if filesize > self.limit*1024*1024:
                message = 'You cannot upload file more than %dMB.' % self.limit
                raise serializers.ValidationError(message)
        elif self.unit == "KB":
            if filesize > self.limit*1024:
                message = 'You cannot upload file more than %dKB.' % self.limit
                raise serializers.ValidationError(message)
            