from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/delete/", views.DeleteView.as_view(), name="delete"),
    path("create/", views.CreateView.as_view(), name="create"),
    path("<int:question_id>/add_choice/", views.AddChoiceView.as_view(), name="add_choice"),
]
