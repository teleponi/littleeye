from django.urls import path, re_path

from . import views

app_name = "issues"

urlpatterns = [
    path(
        "issue/create",
        views.IssueCreateView.as_view(),
        name="issue_create",
    ),
    path(
        "issue/<int:pk>/update",
        views.IssueUpdateView.as_view(),
        name="issue_update",
    ),
    path(
        "issue/<int:pk>/delete",
        views.IssueDeleteView.as_view(),
        name="issue_delete",
    ),
    path(
        "issue/<int:pk>",
        views.IssueDetailView.as_view(),
        name="issue_detail",
    ),
    path("issues", views.IssueListView.as_view(), name="issues"),
]
