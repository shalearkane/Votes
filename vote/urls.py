from django.urls import path
from . import views

urlpatterns = [
    path("", views.vote_page, name="vote_page"),
    path("results/", views.vote_results, name="vote_results"),
    path("clear_votes/", views.clear_votes, name="clear_votes"),
]
