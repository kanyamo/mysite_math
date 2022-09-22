from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('article-create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('article-edit/<int:pk>/', views.ArticleEditView.as_view(), name='article-edit'),
    path('category/<str:inner_name>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('category-create/', views.CategoryCreateView.as_view(), name='category-create'),
    path('category-edit/<str:inner_name>', views.CategoryEditView.as_view(), name='category-edit'),
    path('user-edit/', views.UserEditView.as_view(), name='user-edit'),
    path('user-detail/', views.UserDetailView.as_view(), name='user-detail'),
]