from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.ProjectDetail.as_view()),
    path('create/', views.ProjectCreate.as_view()),
    path("update/<int:pk>/", views.ProjectUpdate.as_view()),
    path('my/', views.ProjectList.as_view()),
    path('', views.ProjectList.as_view()),
]
