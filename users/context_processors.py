from django.contrib.auth import get_user


def user(request):
    user = get_user(request)
    return {'current_user': user}
