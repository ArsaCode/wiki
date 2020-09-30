from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<int:entry_id>", views.page, name="page"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("change/<int:entry_id>", views.edit, name="edit"),
    path("random", views.rand, name="rand")
]
