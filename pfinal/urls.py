from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pfinal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^todas$', 'webapp.views.pag_Todas_Actividades'),
    url(r'^login$', 'webapp.views.login'),
    url(r'^accounts/auth/$', 'webapp.views.auth_view'),
    url(r'^actividad/(\d+)', 'webapp.views.actividades'),
    url(r'^actividad/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.STATIC_URL2}),    
    url(r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^invalid', 'webapp.views.invalid_login'),
    url(r'^add', 'webapp.views.cogerActividad'),
    url(r'^ayuda$', 'webapp.views.ayuda'),
    url(r'^prueba$', 'webapp.views.prueba'),
    url(r'^diezmas$', 'webapp.views.diezMas'),
    url(r'^(.*)/rss', 'webapp.views.cogerRss'),
    url(r'^css/(?P<path>.*)$','django.views.static.serve', {'document_root' : settings.STATIC_URL2}),
    url(r'^$', "webapp.views.init"),
    url(r'^(.*)', 'webapp.views.pag_usuario'),
)
