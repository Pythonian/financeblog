from django.urls import path

from . import views

app_name = 'advice'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='list'),
    path('create/',
         views.QuestionCreateView.as_view(), name='create'),
    path('api/<int:pk>/', views.AdviceListView.as_view()),
    path('api/<int:pk>/create', views.AdviceCreateView.as_view()),
    path('<int:pk>/',
         views.QuestionDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/',
         views.QuestionDeleteView.as_view(), name='delete'),
]
