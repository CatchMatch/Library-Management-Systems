from django.db import models
from django.utils import timezone

# Signup details
class Signup(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    phone_num = models.BigIntegerField()
    password = models.CharField(max_length=50)
    password2 = models.CharField(max_length=50)

    def __str__(self):
        return self.username

# Book details
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

# Book stock
class Stock(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='stock')
    total_copies = models.PositiveIntegerField(default=0)
    available_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.book.title} - {self.available_copies} available"

# Borrow details
class Borrow(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(default=timezone.now)
    due_date = models.DateField()

    def is_overdue(self):
        return timezone.now().date() > self.due_date
    
    def fine_amount(self):
        if self.is_overdue():
            overdue_days = (timezone.now().date() - self.due_date).days
            return overdue_days * 2
        return 0

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
