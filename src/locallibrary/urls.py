from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", RedirectView.as_view(url="/catalog/", permanent=True)),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
)
