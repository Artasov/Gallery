from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signup_confirmation/<str:confirmation_code>/', views.signup_confirmation, name='signup_confirmation'),
    path('signin/', views.signin, name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_confirmation/<str:confirmation_code>/', views.password_reset_confirmation,
         name='password_reset_confirmation'),
    path('about/', TemplateView.as_view(template_name='Core/about.html'), name='about'),
    path('terms_and_conditions/', TemplateView.as_view(template_name='Core/terms_and_conditions.html'),
         name='terms_and_conditions'),
    path('privacy_policy/', TemplateView.as_view(template_name='Core/privacy_policy.html'), name='privacy_policy'),
    path('addresses/', TemplateView.as_view(template_name='Core/addresses.html'), name='addresses'),
    path('contacts/', TemplateView.as_view(template_name='Core/contacts.html'), name='contacts'),
    path('profile/', views.profile, name='profile'),

    path('', views.main, name='main'),
    path('shop/', include(('APP_shop.urls', 'APP_shop'), namespace='shop')),
    path('cart/', include(('APP_cart.urls', 'APP_cart'), namespace='cart'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
