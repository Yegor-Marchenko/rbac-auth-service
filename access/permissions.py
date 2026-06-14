from rest_framework import permissions

from authentication.exceptions import NotAuthenticatedError

from .models import AccessRule


class AccessRulePermission(permissions.BasePermission):
    """
    Проверяет права роли пользователя по таблице AccessRule.
    """
    method_to_action = {
        'GET': 'read',
        'POST': 'create',
        'PUT': 'update',
        'PATCH': 'update',
        'DELETE': 'delete',
    }

    def get_rule(self, request, view):
        """Находит правило доступа для роли пользователя и ресурса вьюхи."""
        resource_name = getattr(view, 'resource_name', None)
        if resource_name is None:
            return None
        return AccessRule.objects.filter(
            role=request.user.role,
            resource__title=resource_name,
        ).first()

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticatedError()

        if request.user.is_superuser:
            return True

        action = self.method_to_action.get(request.method)
        if action is None:
            return False

        rule = self.get_rule(request, view)
        if rule is None:
            return False

        if action == 'read':
            return rule.read_permission or rule.read_all_permission
        flag_name = f'{action}_permission'
        return getattr(rule, flag_name)

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        action = self.method_to_action.get(request.method)
        if action is None:
            return False

        if obj.owner == request.user.id:
            return True

        rule = self.get_rule(request, view)
        if rule is None:
            return False

        flag_name = f'{action}_all_permission'
        return getattr(rule, flag_name)


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticatedError()
        if request.user.is_superuser:
            return True
        return request.user.role is not None and request.user.role.title == 'admin'


class IsAuthenticatedCustom(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticatedError()
        return True
