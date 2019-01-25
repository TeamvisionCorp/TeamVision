from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication (SessionAuthentication):

    def enforce_csrf(self, request):
        if request.path.startswith('/api'):
            return
        else:
            return SessionAuthentication.enforce_csrf(CsrfExemptSessionAuthentication,request)
