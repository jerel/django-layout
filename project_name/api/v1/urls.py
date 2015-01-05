from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from {{ project_name }}.api.v1.resources.identity import Identity


router = DefaultRouter(trailing_slash=False)

router.register(r'identities', Identity)

urlpatterns = router.urls

urlpatterns += [
    url(r'^authenticate', views.obtain_auth_token)
]

