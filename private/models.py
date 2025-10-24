from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from multiselectfield import MultiSelectField

# Create your models here.


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    acct_num = models.CharField(max_length=50, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    account_type = models.CharField(
        max_length=50,
        choices=[
            ("General", "General"),
            ("Cash", "Cash"),
            ("Current", "Current"),
            ("Current account", "Current account"),
            ("Credit card", "Credit card"),
            ("Saving account", "Saving account"),
            ("Investment", "Investment"),
            ("Insurance", "Insurance"),
            ("Bonus", "Bonus"),
            ("Loan", "Loan"),
            ("Mortgage", "Mortgage"),
        ],
    )
    currency = models.CharField(max_length=3)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.currency} {self.balance})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_account_per_user"
            )
        ]


RECORD_TYPE_CHOICES = [
    ("income", "Income"),
    ("expense", "Expense"),
    ("transfer", "Transfer"),
]

CATEGORY_TYPE_CHOICES = [
    ("Salary", "Salary"),
    ("Freelance", "Freelance"),
    ("Investments", "Investments"),
    ("Rental Income", "Rental Income"),
    ("Gifts", "Gifts"),
    ("Refunds", "Refunds"),
    ("Other Income", "Other Income"),
    ("Food & Drinks", "Food & Drinks"),
    ("Groceries", "Groceries"),
    ("Dining Out", "Dining Out"),
    ("Shopping", "Shopping"),
    ("Housing", "Housing"),
    ("Utilities", "Utilities"),
    ("Transportation", "Transportation"),
    ("Vehicle", "Vehicle"),
    ("Life & Entertainment", "Life & Entertainment"),
    ("Communication, PC", "Communication, PC"),
    ("Financial expenses", "Financial expenses"),
    ("Health & Medical", "Health & Medical"),
    ("Education", "Education"),
    ("Insurance", "Insurance"),
    ("Travel", "Travel"),
    ("Gifts & Donations", "Gifts & Donations"),
    ("Personal Care", "Personal Care"),
    ("Subscriptions", "Subscriptions"),
    ("Taxes", "Taxes"),
    ("Savings", "Savings"),
    ("Pets", "Pets"),
    ("Childcare", "Childcare"),
    ("Hobbies", "Hobbies"),
    ("Debt & Loans", "Debt & Loans"),
    ("Repairs & Maintenance", "Repairs & Maintenance"),
    ("Electronics", "Electronics"),
    ("Clothing & Apparel", "Clothing & Apparel"),
    ("Beauty & Wellness", "Beauty & Wellness"),
    ("Books & Media", "Books & Media"),
    ("Office Supplies", "Office Supplies"),
    ("Gardening", "Gardening"),
    ("Sports & Fitness", "Sports & Fitness"),
    ("Weddings & Events", "Weddings & Events"),
    ("Household Supplies", "Household Supplies"),
    ("Legal Fees", "Legal Fees"),
    ("Charity", "Charity"),
    ("Business Expenses", "Business Expenses"),
    ("Others", "Others"),
]

PERIOD_TYPE_CHOICES = [
    ("Week", "Week"),
    ("Month", "Month"),
    ("Year", "Year"),
    ("One-Time", "One Time"),
]


class Record(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1
    )
    record_type = models.CharField(max_length=10, choices=RECORD_TYPE_CHOICES)
    category = models.CharField(max_length=100, choices=CATEGORY_TYPE_CHOICES)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, blank=True, null=True
    )
    from_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="outgoing",
        null=True,
        blank=True,
    )
    to_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="incoming",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    is_recurring = models.BooleanField(default=False)
    recurrence_period = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_record_type_display()} - {self.amount} ({self.category})"

    class Meta:
        indexes = [models.Index(fields=["user", "date"])]


class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ManyToManyField(Account)
    name = models.CharField(max_length=100)
    categories = MultiSelectField(
        "Category", choices=CATEGORY_TYPE_CHOICES, default=list
    )
    period = models.CharField(max_length=100, choices=PERIOD_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def progress(self):
        total_spent = (
            Record.objects.filter(
                user=self.user,
                account__in=self.account.all(),
                category__in=self.categories,
                record_type="expense",
                date__range=(self.start_date, self.end_date),
            ).aggregate(models.Sum("amount"))["amount__sum"]
            or 0
        )

        return (total_spent / self.amount) * 100 if self.amount > 0 else 0

    def __str__(self):
        return self.name

    class Meta:
        indexes = [models.Index(fields=["user", "start_date"])]


SAVE_CHOICES = [
    ("new_vehicle", "New Vehicle"),
    ("new_home", "New Home"),
    ("holiday_trip", "Holiday Trip"),
    ("health_care", "Health Care"),
    ("education", "Education"),
    ("emergency_fund", "Emergency Fund"),
    ("party", "Party"),
    ("kidspoiling", "Kid Spoiling"),
    ("charity", "Charity"),
    ("other", "Other"),
]


class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100, choices=SAVE_CHOICES)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField()
    note = models.TextField(blank=True)

    @property
    def progress_percentage(self):
        return (
            (self.saved_amount / self.target_amount * 100) if self.target_amount else 0
        )

    def __str__(self):
        return self.goal_name


class Debt(models.Model):
    DEBT_TYPE_CHOICES = [
        ("borrowed", "I borrowed"),
        ("lent", "I lent"),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    person = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    debt_type = models.CharField(max_length=100, choices=DEBT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return self.person
