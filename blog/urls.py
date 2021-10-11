from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # path('', views.blog_list, name='list'),
    path('', views.BlogListView.as_view(), name="list"),
    path('blog/create/', views.BlogCreateView.as_view(), name='create'),
    path('blog/<int:pk>/update',
         views.BlogUpdateView.as_view(), name="update"),
    path('blog/<int:pk>/delete',
         views.BlogDeleteView.as_view(), name="delete"),
    path('blog/<int:pk>/',
         views.BlogDetailView.as_view(), name='detail'),
]
