from django.db import models


class ActionChoices(models.TextChoices):
    CREATE = 'create', 'Created Password'
    UPDATE = 'update', 'Updated Password'
    DELETE = 'delete', 'Deleted Password'
    AUDIT = 'audit', 'Performed Audit'
    LOGIN = 'login', 'User Login'
    LOGOUT = 'logout', 'User Logout'
