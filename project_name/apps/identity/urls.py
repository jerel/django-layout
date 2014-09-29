from django.conf.urls import patterns, url, include

# from django.views.generic import TemplateView
import views

password_patterns = patterns('django.contrib.auth.views',
    url(r'^reset/$', 'password_reset',
        kwargs={
            'email_template_name': 'registration/password_reset_email.txt',
        },
        name='password_reset'),
    url(r'^reset/done/$', 'password_reset_done'),
    url(r'^reset/check/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm',
        name='password-reset-confirm'),
    url(r'^complete/$', 'password_reset_complete'),
)

auth_views = patterns(
    'django.contrib.auth.views',
    url(r'^login/$', 'login',
        name='identity-login'),
    url(r'^logout/$', 'logout',
        {'next_page': '/'},
        name='identity-logout'),
    url(r'^register/$', views.Register.as_view(),
        name="identity-register"),
)

urlpatterns = patterns('',
    ('', include(auth_views)),
    (r'^password/', include(password_patterns)),
    url(r'^me/edit/$', views.Edit.as_view(), name='identity-edit'),
)

