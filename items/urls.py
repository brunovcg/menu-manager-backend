from django.urls import path
from .views import ItemsView,ItemsDetailView

urlpatterns = [
    path('items/', ItemsView.as_view()),
    path('items/<int:item_id>/', ItemsDetailView.as_view())
]
