from rest_framework import permissions
from tpo.models import TPR


class TPRPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            TPR.objects.get(name__student__roll = user)
        except TPR.DoesNotExist:
            return False
        return True

class TPOPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_staff

class TPO_TPR_Permissions(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_users = [TPRPermissions(), TPOPermissions()]
        for user_type in allowed_users:
            if user_type.has_permission(request, view):
                return True
        return False

class StudentPlacementPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        student = None
        try:
            student = user.student
        except:
            return False

        try:
            student_placement = student.student_placement
        except:
            return False
        return True

class StudentInternPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        student = None
        try:
            student = user.student
        except:
            return False

        try:
            student_intern = student.student_intern
        except:
            return False
        return True

class StudentNSPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        student = None
        try:
            student = user.student
        except:
            return False

        try:
            student_ns = student.student_ns
        except:
            return False
        return True

class StudentNAPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            student = user.student
        except:
            return False

        other_placements = [StudentNSPermissions(), StudentInternPermissions(), StudentPlacementPermissions()]
        for placement in other_placements:
            if placement.has_permission(request, view):
                return False

        # If the student has no other permissions, allow access to StudentNAPermissions
        return True
    

class PlacementSession(permissions.BasePermission):
    def has_permission(self, request, view):
        other_placements = [StudentNSPermissions(), StudentInternPermissions(), StudentPlacementPermissions()]
        for placement in other_placements:
            if placement.has_permission(request, view):
                return True

        # If the student has no other permissions, allow access to StudentNAPermissions
        return False