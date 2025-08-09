from django.contrib import messages


class ClearAdminMessagesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            list(messages.get_messages(request))

        response = self.get_response(request)
        return response