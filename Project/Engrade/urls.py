from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from Account.views import main_page,Home_page,register,success,logout, troll
from NewQuizzes.views import Create_Quiz,Add_Question,Delete_Title,Edit_Title,Delete_Question,Edit_Question,Assign_to
from classes.views import Create_class,go_to_class,Do_Quizzes,Do_Question,listOfClasses,show_time,Delete_Class


from django.contrib.auth.views import login

from django.conf import settings
import os
site_media=os.path.join(
    os.path.dirname(__file__),'site_media'
)
image = os.path.join(
    os.path.dirname(__file__), 'image'
)

urlpatterns = patterns('',

    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$',logout),
    (r'MainPage/$',main_page),
    (r'^$',Home_page),
    (r'^register/', register),
    (r'^success/$', success),
    (r'^troll/$', troll),



    url(r'^Create_Quizzes/$',Create_Quiz),
    url(r'^Add_Question/(\w+)/$',Add_Question),
    url(r'^Delete_Quiz/(\w+)/$',Delete_Title),
    url(r'^Edit_Quiz/(\w+)/$',Edit_Title),
    url(r'^Delete_Question/(\w+)/$',Delete_Question),
    url(r'^Edit_Question/(\w+)/$',Edit_Question),
    url(r'^Assign_To/(\w+)/$',Assign_to),

    # Examples:
    # url(r'^$', 'Engrade.views.home', name='home'),
    # url(r'^Engrade/', include('Engrade.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^Create_Class/$',Create_class),
    url(r'^go_to_class/(\w+)/$',go_to_class),
    url(r'^Do_Quizzes/(\w+)/$',Do_Quizzes),
    url(r'^Do_Question/(\w+)/$',Do_Question),
    url(r'^ListOfClass/$',listOfClasses),
    url(r'^Delete_Class/(\w+)/$',Delete_Class),
    url(r'^showTime/$',show_time),



    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         { 'document_root': site_media }),

    (r'^image/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': image}),
)
