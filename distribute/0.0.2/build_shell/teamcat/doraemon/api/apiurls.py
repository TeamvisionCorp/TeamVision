#coding=utf-8
from django.conf.urls import  url,include
from django.contrib.auth.models import User,Group
from doraemon.project.models import ProjectMember
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
from doraemon.api.api_render import DoraemonJSONRenderer
import django_filters
from rest_framework import filters
# from doraemon.api.api_filters import APIFitlers


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
#     absolute_url= serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('url','username', 'email', 'is_staff')
    
    def get_absolute_url(self,obj):
        return "fdsdsfdsfds"

# Serializers define the API representation.
class ProjectMemberSerializer(serializers.ModelSerializer):
#     member_full_name= serializers.SerializerMethodField()
#     member_email= serializers.SerializerMethodField()
    class Meta:
        model = ProjectMember
        fields = ('url','PMProjectID','PMRoleID','PMRoleType','PMMember')
    
    def get_member_full_name(self,obj):
        user=User.objects.get(id=obj.PMMember)
        return user.last_name+user.first_name
    
    def get_member_email(self,obj):
        user=User.objects.get(id=obj.PMMember)
        return user.email

# ViewSets define the view behavior.
class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all().filter(PMProjectID=14)
    serializer_class = ProjectMemberSerializer
    
    @list_route()
    def recent_users(self, request):
        recent_users = ProjectMember.objects.all()

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    

    



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'username', 'password', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }
        read_only_fields = ('id',)



class UserProfileView(generics.ListAPIView):
    """
    An endpoint for users to view and update their profile information.
    """
    serializer_class = UserProfileSerializer
    permission_classes=(AllowAny,)
    filter_fields = ('username','is_active')
#     filter_class = APIFitlers
    

#     def get_object(self):
#         id =int(self.kwargs['id'])
#         return User.objects.get(id=id)
    
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        return User.objects.all()

    
#     def get_renderers(self):
#         return [DoraemonJSONRenderer(self.code,self.message)]
    
#     def list(self,request):
#         serialzer=self.serializer_class(self.get_queryset(),many=True)
#         try:
#             serialzer.is_valid()
#             print(serialzer.errors)
#         except Exception as ex:
#             self.code=2
#             self.message=3
#             print(ex)
#         print(serialzer.data)
#         return Response(serialzer.data)


class UserProfileListView(generics.ListAPIView):
    """
    An endpoint for users to view and update their profile information.
    """

    serializer_class = UserProfileSerializer
    permission_classes=(IsAuthenticatedOrReadOnly,)
    
#     def get_queryset(self):
#         """
#         This view should return a list of all the purchases for
#         the user as determined by the username portion of the URL.
#         """
#         return User.objects.all()

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
    url(r'^docs/', include_docs_urls(title='Teamcat API')),
    url(r'project/', include('doraemon.api.project.urlrouter.project_urls')),
    url(r'home/', include('doraemon.api.home.urlrouter.home_urls')),
    url(r'logcat/', include('doraemon.api.logcat.urlrouter.logcat_urls')),
    url(r'ci/', include('doraemon.api.ci.urlrouter.ci_urls')),
    url(r'interface/', include('doraemon.api.interface.urlrouter.interface_urls')),
    url(r'auth/', include('doraemon.api.auth.urlrouter.auth_urls')),
    url(r'common/', include('doraemon.api.common.urlrouter.common_urls')),
    ]