from django.shortcuts import render
from .forms import (
    AccountForm,
    RecordForm,
    RecordUpdateForm,
    BudgetForm,
    GoalForm,
    ProfileUpdateForm,
)
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from django.contrib.auth.decorators import login_required
from .models import Account, Record, Budget, Goal
from django import forms
from django.shortcuts import redirect
from public.models import CustomUser
from rest_framework import generics, permissions
from .serializers import AccountSerializer, RecordSerializer, BudgetSerializer
from rest_framework import generics, permissions


@login_required
def home_view(request):
    accounts = Account.objects.filter(user=request.user)
    context = {"accounts": accounts}
    return render(request, "private/home.html", context)


class AccountView(LoginRequiredMixin, CreateView):
    form_class = AccountForm
    template_name = "private/Account.html"
    success_url = reverse_lazy("dashboard")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AccountDetailView(LoginRequiredMixin, DetailView):
    form_class = AccountForm
    model = Account
    template_name = "private/Account_detail.html"
    context_object_name = "account"

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    form_class = AccountForm
    model = Account
    template_name = "private/Account_edit.html"
    success_url = reverse_lazy("dashboard")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        del form.fields["balance"]
        form.fields["is_active"] = forms.BooleanField(
            required=False,
            label="is active",
            widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
        )
        return form

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = "private/Account_delete.html"
    success_url = reverse_lazy("dashboard")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountListCreateAPI(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class RecordView(LoginRequiredMixin, ListView):
    model = Record
    template_name = "private/record_list.html"
    context_object_name = "records"

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user).order_by("-date")


class RecordListCreateAPI(generics.ListCreateAPIView):
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecordDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)


class RecordAddView(LoginRequiredMixin, CreateView):
    model = Record
    form_class = RecordForm
    template_name = "private/record.html"
    success_url = reverse_lazy("records")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["account"].queryset = Account.objects.filter(user=self.request.user)
        form.fields["from_account"].queryset = Account.objects.filter(
            user=self.request.user
        )
        form.fields["to_account"].queryset = Account.objects.filter(
            user=self.request.user
        )
        return form

    def form_valid(self, form):

        form.instance.user = self.request.user
        record = form.save(commit=False)

        if record.record_type == "expense":
            if record.account:
                record.account.balance -= record.amount
                record.account.save()
        elif record.record_type == "income":
            if record.account:
                record.account.balance += record.amount
                record.account.save()
        elif record.record_type == "transfer":
            if record.from_account and record.to_account:
                record.from_account.balance -= record.amount
                record.to_account.balance += record.amount
                record.from_account.save()
                record.to_account.save()

        if not record.date:
            record.date = timezone.now().date()
        if not record.time:
            record.time = timezone.now().time()

        record.save()
        return super().form_valid(form)


class RecordUpdateView(LoginRequiredMixin, UpdateView):
    form_class = RecordUpdateForm
    model = Record
    template_name = "private/Record_edit.html"
    success_url = reverse_lazy("records")

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields["note"].widget = forms.Textarea(
            attrs={"class": "form-control", "rows": 2, "placeholder": "Optional note"}
        )
        form.fields["date"].widget = forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        )
        form.fields["time"].widget = forms.TimeInput(
            attrs={"type": "time", "class": "form-control"}
        )

        form.fields["account"].queryset = Account.objects.filter(user=self.request.user)
        form.fields["from_account"].queryset = Account.objects.filter(
            user=self.request.user
        )
        form.fields["to_account"].queryset = Account.objects.filter(
            user=self.request.user
        )
        return form

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        record = form.save(commit=False)

        old_record = Record.objects.get(pk=self.object.pk)
        if old_record.record_type == "expense" and old_record.account:
            old_record.account.balance += old_record.amount
            old_record.account.save()

        elif old_record.record_type == "income" and old_record.account:
            old_record.account.balance -= old_record.amount
            old_record.account.save()

        elif (
            old_record.record_type == "transfer"
            and old_record.from_account
            and old_record.to_account
        ):
            old_record.from_account.balance += old_record.amount
            old_record.to_account.balance -= old_record.amount
            old_record.from_account.save()
            old_record.to_account.save()

        if record.record_type == "expense" and record.account:
            record.account.balance -= record.amount
            record.account.save()
        elif record.record_type == "income" and record.account:
            record.account.balance += record.amount
            record.account.save()
        elif (
            record.record_type == "transfer"
            and record.from_account
            and record.to_account
        ):
            record.from_account.balance -= record.amount
            record.to_account.balance += record.amount
            record.from_account.save()
            record.to_account.save()

        if not record.date:
            record.date = timezone.now().date()
        if not record.time:
            record.time = timezone.now().time()

        record.save()
        return super().form_valid(form)


class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Record
    template_name = "private/Record_delete.html"
    success_url = reverse_lazy("records")

    def get_queryset(self):
        return Record.objects.filter(user=self.request.user)


class BudgetListCreateAPI(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetRetrieveUpdateDestroyAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "private/budget.html"
    success_url = reverse_lazy("budget-list")

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BudgetForm
    model = Budget
    template_name = "private/budget_edit.html"
    success_url = reverse_lazy("budget-list")

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = "private/budget_delete.html"
    success_url = reverse_lazy("budget-list")

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = "private/goal.html"
    success_url = reverse_lazy("goal-list")

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def form_valid(self, form):
        goal = form.save(commit=False)
        goal.user = self.request.user

        if form.cleaned_data.get("goal_name") == "other" and form.cleaned_data.get(
            "custom_goal_name"
        ):
            goal.goal_name = form.cleaned_data["custom_goal_name"]

        goal.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUpdateForm
    template_name = "private/profile.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = "private/budget_list.html"
    context_object_name = "budgets"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).order_by("-created_at")


class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = "private/goal_list.html"
    context_object_name = "goals"

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by("-date")


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = "private/goal_edit.html"
    success_url = reverse_lazy("goal-list")

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = "private/goal_delete.html"
    success_url = reverse_lazy("goal-list")

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
