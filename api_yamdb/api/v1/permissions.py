from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnlyOrIsAdminOrModeratorOrAuthor(BasePermission):
    message = ('Ошибка прав доступа!'
               'Действие доступно только для администратора, модератора '
               'или автора.')

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user.is_moderator
                or request.user.is_admin or request.user == obj.author)


class IsAdmin(BasePermission):
    message = ('Ошибка прав доступа!'
               'Действие доступно только для администратора.')

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_staff
                     or request.user.is_superuser)
                )


class IsAdminOrReadOnly(BasePermission):
    message = ('Ошибка прав доступа! '
               'Действие доступно только для администратора.')

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False


class AuthorAndModerator(BasePermission):
    message = ('Ошибка прав доступа!'
               'Действие доступно только для модератора или автора.')

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.is_moderator)
                    )
                )
