#coding=utf-8
from django.conf.urls import  url,include
from django.contrib.auth.models import User,Group
from teamvision.project.models import ProjectMember
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import parsers, renderers, generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
import oauth2_provider.views as oauth2_views
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from rest_framework.compat import unicode_to_repr
from rest_framework.exceptions import ValidationError
from rest_framework.utils.representation import smart_repr
from teamvision.api.api_render import TeamvisionJSONRenderer
import django_filters
from rest_framework import filters




class LoginView(APIView):
    """
    A view that allows users to login providing their username and password.
    """

    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        url(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        url(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        url(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        url(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        url(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        url(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        url(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


urlpatterns = [
#     url(r'^login/$', LoginView.as_view(), name="login"),
#     url(r'user/profiles/(?P<id>.+)/$', UserProfileView.as_view(), name="profile"),
#     url(r'user/profiles', UserProfileView.as_view(), name="profile-list"),
#     url(r'posts', PostView.as_view(), name="post-list"),
    url(r'^o/', include((oauth2_endpoint_views,'oauth2_provider'), namespace='oauth2_provider')),
    url(r'^docs/', include_docs_urls(title='Teamvision API')),
    url(r'project/', include('teamvision.api.project.urlrouter.project_urls')),
    url(r'home/', include('teamvision.api.home.urlrouter.home_urls')),
    url(r'logcat/', include('teamvision.api.logcat.urlrouter.logcat_urls')),
    url(r'ci/', include('teamvision.api.ci.urlrouter.ci_urls')),
    url(r'interface/', include('teamvision.api.interface.urlrouter.interface_urls')),
    url(r'auth/', include('teamvision.api.auth.urlrouter.auth_urls')),
    url(r'common/', include('teamvision.api.common.urlrouter.common_urls')),
    ]