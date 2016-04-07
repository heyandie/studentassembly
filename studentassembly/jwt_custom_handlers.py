from account.models import User

def jwt_get_username_from_payload(payload):
    """
    Override this function if username is formatted differently in payload
    """
    try:
        alias = payload.get('alias')
        return User.objects.get(username=alias).email
    except:
        return None
