from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView

# Overriding AdminSite attributes.
admin.site.site_header = admin.site.site_title = "MUTATIO"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("admin:index"))),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
