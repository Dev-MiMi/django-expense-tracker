from django.urls import path
from .views import (
    home_view,
    AccountView,
    AccountDetailView,
    AccountUpdateView,
    AccountDeleteView,
    RecordView,
    RecordAddView,
    RecordUpdateView,
    RecordDeleteView,
    BudgetCreateView,
    BudgetUpdateView,
    BudgetDeleteView,
    BudgetListView,
    GoalCreateView,
    GoalUpdateView,
    GoalDeleteView,
    GoalListView,
    ProfileView
)

urlpatterns = [
    path("home/", home_view, name="dashboard"),
    path("accounts/", AccountView.as_view(), name="account"),
    path("accounts/<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
    path("accounts/<int:pk>/edit/", AccountUpdateView.as_view(), name="account-edit"),
    path(
        "accounts/<int:pk>/edit/delete/",
        AccountDeleteView.as_view(),
        name="account-delete",
    ),
    path("records/", RecordView.as_view(), name="records"),
    path("records/add/", RecordAddView.as_view(), name="record-add"),
    path(
        "records/<int:pk>/edit/", RecordUpdateView.as_view(), name="record-detail-edit"
    ),
    path(
        "records/<int:pk>/edit/delete/",
        RecordDeleteView.as_view(),
        name="record-delete",
    ),
    path(
        "budgets/<int:pk>/edit/delete/",
        BudgetDeleteView.as_view(),
        name="budget-delete",
    ),
    path(
        "budget/<int:pk>/edit/",
        BudgetUpdateView.as_view(),
        name="budget-detail-edit",
    ),
    path(
        "budgets/",
        BudgetListView.as_view(),
        name=("budget-list"),
    ),
    path(
        "budgets/add/",
        BudgetCreateView.as_view(),
        name=("budget-add"),
    ),
    path(
        "goals/<int:pk>/edit/delete/",
        GoalDeleteView.as_view(),
        name="goal-delete",
    ),
    path(
        "goals/<int:pk>/edit/",
        GoalUpdateView.as_view(),
        name="goal-detail-edit",
    ),
    path(
        "goals/",
        GoalListView.as_view(),
        name=("goal-list"),
    ),
    path(
        "goals/add/",
        GoalCreateView.as_view(),
        name=("goal-add"),
    ),
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"),
]
