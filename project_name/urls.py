from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^api/1.0/', include('{{ project_name }}.api.v1.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    # url('', include('{{ project_name }}.apps.')),
)
