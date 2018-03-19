"""aliennorDjangoBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from ecocases import views

router = DefaultRouter()
# router.register(r'ecocases', views.get_ecocases, base_name='api_ecocase')
router.register(r'comments', views.EcocaseCommentViewSet, base_name='api_ecocase_comment')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/ecocases/', include('ecocases.urls', namespace='ecocases')),
    url(r'^api/esms/(?P<esm_id>[0-9]+)/$', views.get_esm_by_id, name='get_esm_by_id'),
    url(r'^api/esms/$', views.get_esms, name='get_esms'),
    url(r'^api/esms/(?P<esm_id>[0-9]+)/ecocases$', views.get_ecocases_by_esm, name='get_ecocases_by_esm'),
    url(r'^api/auth/csrf$', views.send_csrf, name='send csrf token'),
    url(r'^api/auth/login/$', views.login, name='login'),
    url(r'^api/auth/register/$', views.register, name='register'),
    url(r'^api/auth/username-exists/$', views.username_exists, name='check unique username'),
    url(r'^api/user/get-data/$', views.get_user_data, name='get user data'),
    url(r'^api/user/update/$', views.update_data, name='update user data'),
    url(r'^api/user/update-password/$', views.update_password, name='update user password'),
    url(r'^api/user/delete/$', views.delete_account, name='delete user account')
]