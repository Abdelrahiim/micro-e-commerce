from Micro.products.views import ProductAttachmentDownLoadView, ProductCreateView, ProductDetailView,ProductListView
from django.urls import path

app_name = 'product'
urlpatterns = [
    path('create/',ProductCreateView.as_view(),name = "create"),
    path('list/',ProductListView.as_view(),name = "list"),
    path('download/',ProductAttachmentDownLoadView.as_view(),name = "download"),
    path('<slug:handle>/',ProductDetailView.as_view(),name = "detail"),
]
