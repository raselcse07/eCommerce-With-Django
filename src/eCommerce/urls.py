from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include("products.urls")),
    path('search/', include("search.urls")),
    path('cart/', include("cart.urls")),
    path('accounts/', include("accounts.urls")),
    path('address/', include("address.urls")),
    path('billing/', include("billing.urls")),
    path('', include("home.urls")),

]


if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)