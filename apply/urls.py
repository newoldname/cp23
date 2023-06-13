from django.urls import path
from . import views

urlpatterns = [
    # path("<int:pk>/", views.ApplicationDetail.as_view()),

    path("choose/<int:projectPk>/", views.selectPeople),
    path("create/<int:projectPk>/", views.ApplicationCreate.as_view()),
    path("update/<int:pk>/", views.ApplicationUpdate.as_view()),
    path("list/<int:projectPk>/", views.ApplicationList.as_view()),
    # path("update/<int:pk>/", views.ApplicationUpdate.as_view()),
    path('my/', views.ApplicationList.as_view()),
]
