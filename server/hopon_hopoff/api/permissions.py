from rest_framework.permissions import BasePermission, SAFE_METHODS
from database.models import Permission, UserPermission, RolePermission

def HasPermission(code):
    class CustomPermission(BasePermission):
        def has_permission(self, request, view):
            if not request.user or not request.user.is_authenticated:
                return False
            
            user = request.user
            # Kiểm tra user-permission trực tiếp
            if UserPermission.objects.filter(user=user, code=code).exists():
                return True
            # Kiểm tra qua role
            try:
                role = user.userprofile.role
                return RolePermission.objects.filter(   
                    role=role, permission__code=code
                ).exists()
            except:
                return False
            
    return CustomPermission


class IsAdmin(BasePermission):
    """
    Permission to check if the user is an admin.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin
        

class IsOwner(BasePermission):
    """
    Permission to check if the user is the owner of the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsAuthorOrReadOnly(BasePermission):
    """
    Permission to check if the user is the author of the object or has read-only access.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the request method is safe (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Check if the user is the author of the object
        return obj.author == request.user
    
