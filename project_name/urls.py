from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^identity/', include('{{ project_name }}.apps.identity'),
    # url('', include('{{ project_name }}.apps.')),
)
