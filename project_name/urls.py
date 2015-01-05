from django.conf.urls import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/1.0/', include('{{ project_name }}.api.v1.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url('', include('{{ project_name }}.apps.')),
)
