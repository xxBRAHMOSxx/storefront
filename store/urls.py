from django.urls import path
from . import views

# url configuration
urlpatterns = [
    path("products/", views.product_list),
    path("products/<int:id>/", views.product_detail),
    path("collections/<int:pk>/", views.collection_detail,
         name="collection-detail"),
]
