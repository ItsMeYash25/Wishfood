from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

admin.site.site_header = "Wish-food"
admin.site.site_title = "Wish-food Admin "
admin.site.index_title = "Welcome to Wish-food"

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('Home.urls')),
    path('Account/', include('Account.urls')),
    path('store/', include('store.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'Home.views.error_404_view'
