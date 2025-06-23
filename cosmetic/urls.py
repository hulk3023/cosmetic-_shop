
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from beauty.views import login_registration
from  cosmetic import  settings
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('beauty.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='beauty/login_registration.html'), name='login'),

    path('pyclick/', include('pyclick.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)