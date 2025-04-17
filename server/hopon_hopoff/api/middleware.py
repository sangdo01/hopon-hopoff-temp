from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from database.models import User, Role, Permission, UserPermission, RolePermission, UserRole

def has_permission(user, code):
    """
    Check if the user has the specified permission code.
    """
    if not user or not user.is_authenticated:
        return False
    # Check direct user-permission
    if UserPermission.objects.filter(user=user, permission__code=code).exists():
        return True
    
    # Check through role
    try:
        role = user.userrole.role
        return RolePermission.objects.filter(role=role, permission__code=code).exists()
    except UserRole.role.RelatedObjectDoesNotExist:
        return False
    
class PermissionMiddleware:
    """
    Middleware to check user permissions for specific views.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # add path → permission mapping here
        self.permission_map = {
            '/api/tours/create/': 'can_create_tour',
            '/api/tours/delete/': 'can_delete_tour',
            '/api/tours/update/': 'can_update_tour',
        }

    def __call__(self, request):
        # Get the view and method from the request
        # view = request.resolver_match.view_name
        # method = request.method
        
        # # Define permission codes based on view and method
        # permission_codes = {
        #     'tour': {
        #         'GET': 'view_tour',
        #         'POST': 'add_tour',
        #         'PUT': 'change_tour',
        #         'DELETE': 'delete_tour'
        #     },
        #     'user': {
        #         'GET': 'view_user',
        #         'POST': 'add_user',
        #         'PUT': 'change_user',
        #         'DELETE': 'delete_user'
        #     }
        # }
        
        # # Check if the view is in the permission codes
        # if view in permission_codes:
        #     code = permission_codes[view].get(method)
        #     if code and not has_permission(request.user, code):
        #         return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # Check if the request path is in the permission map
        path = request.path
        if path in self.permission_map:
            code = self.permission_map[path]
            if not has_permission(request.user, code):
                return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        response = self.get_response(request)
        return response