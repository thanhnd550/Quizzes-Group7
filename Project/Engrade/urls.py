from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from Quizzes.views import Add_Quiz,DELETE,EDIT,DISPLAY
from Account.views import main_page,Home_page,register,success,logout
from NewQuizzes.views import Create_Quiz,Add_Question,Delete_Title,Edit_Title,Delete_Question,Edit_Question
from django.contrib.auth.views import login

from django.conf import settings
import os.path
site_media=os.path.join(
    os.path.dirname(__file__),'site_media'
)


urlpatterns = patterns('',
    url(r'^Quizzes/',Add_Quiz),
    url(r'^Delete/(\w+)/$',DELETE),
    url(r'^Edit/(\w+)/$',EDIT),
    url(r'^Display/(\w+)/$',DISPLAY),

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$',logout),
    (r'MainPage/$',main_page),
    (r'home_page/$',Home_page),
    (r'^register/', register),
    (r'^success/$', success),


    url(r'^Create_Quizzes/$',Create_Quiz),
    url(r'^Add_Question/(\w+)/$',Add_Question),
    url(r'^Delete_Quiz/(\w+)/$',Delete_Title),
    url(r'^Edit_Quiz/(\w+)/$',Edit_Title),
    url(r'^Delete_Question/(\w+)/$',Delete_Question),
    url(r'^Edit_Question/(\w+)/$',Edit_Question),

    # Examples:
    # url(r'^$', 'Engrade.views.home', name='home'),
    # url(r'^Engrade/', include('Engrade.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': site_media }),

)
