from django.urls import path

from . import views

app_name = "issues"

urlpatterns = [
    path("", views.IssueListView.as_view(), name="issues"),
    path(
        "ticket/comment/<int:issue_id>",
        views.CommentCreateView.as_view(),
        name="comment_create",
    ),
    path(
        "ticket/comment/show/<int:pk>",
        views.CommentDetailView.as_view(),
        name="comment_detail",
    ),
    path(
        "ticket/history/<int:issue_id>",
        views.IssueHistoryListView.as_view(),
        name="issue_history",
    ),
    path(
        "create",
        views.IssueCreateView.as_view(),
        name="issue_create",
    ),
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
    path(
        "ticket/<int:pk>",
        views.IssueDetailTutorView.as_view(),
        name="issue_detail_tutor",
    ),
    path(
        "ticket/<int:pk>/update",
        views.IssueUpdateTutorView.as_view(),
        name="issue_update_tutor",
    ),
]
