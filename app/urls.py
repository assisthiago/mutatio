from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView

import app.core.views

urlpatterns = [
    path("", app.core.views.index, name="index"),
    path("sign-in", app.core.views.signin, name="sign-in"),
    path("sign-out", app.core.views.signout, name="sign-out"),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
