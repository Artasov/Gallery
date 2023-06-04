from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('upload_products/', views.upload_products, name='upload_products'),
    path('get_favorite_products_bt_names/', views.get_favorite_products_bt_names, name='get_favorite_products_bt_names'),

    path('favorites/', TemplateView.as_view(template_name='APP_shop/favorites.html'), name='favorites'),

    path('get_new_for_pagination/<int:last_pag_num>/', views.get_new_for_pagination, name='get_new_for_pagination'),
    path('product/<int:id>/', views.product_detail,
         name='product_detail')
]
