from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", RedirectView.as_view(url="/superadmin/", permanent=False)),
    path("superadmin/", admin.site.urls),  # Keep legacy alias
    path("accounts/", include("apps.accounts.urls")),
    path("menu/", include("apps.menu.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("orders/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
    path("reports/", include("apps.reports.urls")),
    path("platform/", include("apps.platform_admin.urls")),
    path("", RedirectView.as_view(pattern_name="dashboard:index", permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
