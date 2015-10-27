from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
	url(r'',include('mysite.cheungssh.urls')),
    	url(r'^cheungssh/admin/', include(admin.site.urls)),
)
