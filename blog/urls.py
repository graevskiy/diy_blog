"""diy_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    # path('blogs/', cache_page(60 * 5)(views.BlogListView.as_view()), name='blogs'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('create/', views.BlogPostCreateView.as_view(), name='create-blog'),    
    path('<int:pk>/', views.BlogDetailView.as_view(), name='blog'),
    
    path('categories/', views.CategoriesListView.as_view(), name='categories'),
    path('category/<int:pk>/', views.BlogListByCategoryView.as_view(), name='blogs_of_category'),
    
    path('comment/<int:pk>/update/', views.CommentEditView.as_view(), name='edit-comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),

    path('authors/', views.AuthorsListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author'),
]
