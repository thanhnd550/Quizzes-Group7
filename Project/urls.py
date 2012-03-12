from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import login, logout
import polls
import os.path
from Quizz.polls.views import main_page,Home_page

admin.autodiscover()
site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns('',(r'login/$',login),
    (r'accounts/logout/$',logout),
    (r'MainPage/$',main_page),
    (r'home_page/$',Home_page),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': site_media }),
    #(r'accounts/show/$','templates.show.html'),
    # Examples:
    # url(r'^$', 'Quizz.views.home', name='home'),
    # url(r'^Quizz/', include('Quizz.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)
