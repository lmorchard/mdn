from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

import jingo


admin.autodiscover()

def _error_page(request, status):
    """Render error pages with jinja2."""
    return jingo.render(request, '%d.html' % status, status=status)
handler404 = lambda r: _error_page(r, 404)
handler500 = lambda r: _error_page(r, 500)


urlpatterns = patterns('',
    # Home / landing pages:
    ('', include('landing.urls')),
    ('', include('docs.urls')),
    (r'^demos/', include('demos.urls')),

    # Django admin:
    (r'^admin/', include(admin.site.urls)),
)
if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

