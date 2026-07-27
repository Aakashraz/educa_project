from rest_framework.permissions import BasePermission



# has_permission() - A view-level permission check
# has_object_permission() - An object-level permission check
class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()