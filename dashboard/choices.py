from django.db import models


class ActionChoices(models.TextChoices):
    CREATE = 'create', 'Created Password'
    UPDATE = 'update', 'Updated Password'
    DELETE = 'delete', 'Deleted Password'
    VIEW = 'view', 'Viewed Password'
    AUDIT = 'audit', 'Performed Audit'
    LOGIN = 'login', 'User Login'
    LOGOUT = 'logout', 'User Logout'
