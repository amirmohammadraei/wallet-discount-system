from django.db import models


class User(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.mobile_number

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.mobile_number}'s Wallet"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_of_transaction = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.mobile_number} - {self.amount} ({self.type}) at {self.timestamp}"

class DiscountCode(models.Model):
    CODE_TYPE_CHOICES = [
        ('DISCOUNT', 'Discount Code'),
        ('CHARGING', 'Charging Code'),
    ]

    code = models.CharField(max_length=20, unique=True)
    code_type = models.CharField(max_length=10, choices=CODE_TYPE_CHOICES)
    count = models.PositiveIntegerField(default=1)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.get_code_type_display()}: {self.code}"

class DiscountUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} used {self.discount_code.code} at {self.timestamp}"
