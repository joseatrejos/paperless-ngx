from django.contrib.auth import get_user_model

User = get_user_model()


def normalize_roles(raw_roles):
    return {str(role).strip() for role in raw_roles if str(role).strip()}


def get_user_by_id(user_id):
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return None
