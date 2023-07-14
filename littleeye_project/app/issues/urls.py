from django.urls import path, re_path

from . import views

app_name = "issues"

urlpatterns = [
    path(
        "issue/comment/<int:issue_id>",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "issue/history/<int:issue_id>",
        views.IssueHistoryListView.as_view(),
        name="issue_history",
    ),
    path(
        "create",
        views.IssueCreateView.as_view(),
        name="issue_create",
    ),
    # path(
    # "<int:pk>/update",
    # views.IssueUpdateView.as_view(),
    # name="issue_update",
    # ),
    path(
        "<int:pk>/delete",
        views.IssueDeleteView.as_view(),
        name="issue_delete",
    ),
    path(
        "<int:pk>",
        views.IssueDetailView.as_view(),
        name="issue_detail",
    ),
    path("", views.IssueListView.as_view(), name="issues"),
    path(
        "issue/<int:pk>",
        views.IssueDetailTutorView.as_view(),
        name="issue_detail_tutor",
    ),
    path(
        "issue/<int:pk>/update",
        views.IssueUpdateTutorView.as_view(),
        name="issue_update_tutor",
    ),
]
