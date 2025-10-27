from django import forms
from .models import (
    Account,
    Record,
    RECORD_TYPE_CHOICES,
    CATEGORY_TYPE_CHOICES,
    Budget,
    SAVE_CHOICES,
    Goal,
    Debt,
    PERIOD_TYPE_CHOICES,
)
import pycountry
from django_select2.forms import Select2Widget
from datetime import timedelta, date
from public.models import CustomUser
from django.core.exceptions import ValidationError

# account form page
class AccountForm(forms.ModelForm):
    balance = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        initial=0,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "inputmode": "decimal",
                "pattern": "-?[0-9]*[.,]?[0-9]+",
                "min": "-999999",
                "step": "0.01",
            }
        ),
        label="Current Balance",
    )

    account_type = forms.ChoiceField(
        choices=Account._meta.get_field("account_type").choices,
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Type of Account",
    )

    currency = forms.ChoiceField(
        choices=[
            (c.alpha_3, f"{c.name} ({c.alpha_3})")
            for c in sorted(pycountry.currencies, key=lambda c: c.name)
        ],
        widget=forms.Select(attrs={"class": "form-select"}),
        initial="NGN",
    )

    class Meta:
        model = Account
        fields = ["name", "acct_num", "balance", "account_type", "currency"]
        labels = {
            "name": "Account Name",
            "acct_num": "Account Number",
            "balance": "Current Balance",
            "account_type": "Type of Account",
            "currency": "Currency Code",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "acct_num": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        user = self.current_user or getattr(self.instance, "user", None)
        if (
            user
            and Account.objects.filter(user=user, name__iexact=name)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("You already have an account with this name.")
        return name

# record form page
class RecordForm(forms.ModelForm):
    record_type = forms.ChoiceField(
        choices=RECORD_TYPE_CHOICES,
        widget=Select2Widget(attrs={"class": "form-select"}),
        label="Record Type",
    )

    category = forms.ChoiceField(
        choices=CATEGORY_TYPE_CHOICES,
        widget=Select2Widget(attrs={"class": "form-select"}),
        label="Category",
    )

    class Meta:
        model = Record
        fields = [
            "record_type",
            "category",
            "account",
            "from_account",
            "to_account",
            "amount",
        ]
        labels = {
            "amount": "Amount",
            "from_account": "From Account",
            "to_account": "To Account",
            "accounts": "Accounts (for splits)",
        }
        widgets = {
            "accounts": forms.SelectMultiple(attrs={"class": "form-select"}),
            "from_account": forms.Select(attrs={"class": "form-select"}),
            "to_account": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "inputmode": "decimal",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Optional note",
                }
            ),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["account"].required = False
        self.fields["from_account"].required = False
        self.fields["to_account"].required = False

    def clean(self):
        cleaned_data = super().clean()
        record_type = cleaned_data.get("record_type")
        account = cleaned_data.get("account")
        from_account = cleaned_data.get("from_account")
        to_account = cleaned_data.get("to_account")

        if record_type in ["income", "expense"]:
            if not account:
                raise ValidationError(
                    "Account is required for income or expense records."
                )
            cleaned_data["from_account"] = None
            cleaned_data["to_account"] = None

        elif record_type == "transfer":
            if not from_account or not to_account:
                raise ValidationError(
                    "Both from_account and to_account are required for transfers."
                )
            cleaned_data["account"] = None

        return cleaned_data

# record edit form page
class RecordUpdateForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            "record_type",
            "account",
            "from_account",
            "to_account",
            "amount",
            "note",
            "date",
            "time",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ["account", "from_account", "to_account"]:
            self.fields[field].required = False
            self.fields[field].empty_label = None


from django_select2.forms import Select2MultipleWidget

# budget form page
class BudgetForm(forms.ModelForm):
    currency = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Budget
        fields = [
            "name",
            "categories",
            "period",
            "start_date",
            "end_date",
            "amount",
            "currency",
            "account",
        ]
        widgets = {
            "categories": Select2MultipleWidget(),
            "account": Select2MultipleWidget(),
            "period": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        self.fields["period"].required = True
        self.fields["period"].choices = [
            (k, v) for k, v in PERIOD_TYPE_CHOICES if k != ""
        ]

        self.fields["categories"].choices = CATEGORY_TYPE_CHOICES
        self.fields["categories"].required = True

        if user is not None:
            self.fields["account"].queryset = Account.objects.filter(user=user)
            currencies = (
                Account.objects.filter(user=user)
                .values_list("currency", flat=True)
                .distinct()
            )
            self.fields["currency"].initial = list(currencies)[0] if currencies else ""
        else:
            self.fields["account"].queryset = Account.objects.none()
            self.fields["currency"].initial = ""

    def clean(self):
        cleaned = super().clean()
        accounts = cleaned.get("account")
        currency = cleaned.get("currency")

        if accounts:
            currencies = {acc.currency for acc in accounts}
            if len(currencies) > 1:
                raise forms.ValidationError(
                    "All selected accounts must use the same currency."
                )

            if currency and (currency not in currencies):
                raise forms.ValidationError("Currency must match selected account(s).")

            if not currency:
                cleaned["currency"] = next(iter(currencies))
        return cleaned

# goal form page
class GoalForm(forms.ModelForm):
    custom_goal_name = forms.CharField(
        required=False,
        label="Custom Goal Name",
        help_text="Enter your goal if it's not in the list.",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Goal
        fields = [
            "goal_name",
            "custom_goal_name",
            "target_amount",
            "saved_amount",
            "target_date",
            "note",
        ]
        widgets = {
            "goal_name": forms.Select(attrs={"class": "form-select"}),
            "target_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "saved_amount": forms.NumberInput(attrs={"class": "form-control"}),
            "target_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "note": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
