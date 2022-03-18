from django.urls import path
from .views import CategoriesView,CategoriesDetailView

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('categories/<int:category_id>/', CategoriesDetailView.as_view())
]
