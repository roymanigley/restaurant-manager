from django.contrib.sessions.models import Session
from rest_framework.authentication import BaseAuthentication


class CustomSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        session_key = request.COOKIES.get('sessionid')
        if not session_key:
            return None

        try:
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('_auth_user_id')
            if not user_id:
                return None

            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(pk=user_id)
            return (user, None)
        except:
            return None
