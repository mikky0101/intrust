from urllib import request
from django.db import models
from django.db.models.signals import post_save,pre_save
import secrets
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number = models.IntegerField(blank=True, null=True)
    middle_name = models.CharField(max_length=15, blank=True, null=True)
    account_type = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='images/', blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=8, blank=True, null=True)
    account_balance = models.CharField(max_length=15, blank=True, null=True)
    pin = models.CharField(max_length=4, default=0000)

    def get_balance(self):
        bal = float(self.account_balance.replace(',', ""))
        return float(bal)

    def get_user_profile(self):
        return reverse("main:profile", kwargs={
            "pk": self.id
        })

    def get_history(self):
         return reverse("main:history", kwargs={
             "us": self.username
         })

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=20, blank=True, null=True)
    code = models.CharField(max_length=4)
    bank_name = models.CharField(max_length=30)


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Transaction(models.Model):
    ref = models.CharField(max_length=200)
    amount_tf = models.CharField(max_length=10)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE)
    successful = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.sender.username

    def get_confirmation_url(self):
        return reverse("main:confirm", kwargs={
            'ref': self.ref
        })

    def get_details(self):
         return reverse("main:details", kwargs={
             "ref": self.ref
         })

    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Transaction.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)



def user_balance_signal(sender, instance, created, **kwargs):
    print(instance)
    user = User.objects.get(username = instance.sender.username)
    print(user)
    print(user)
    user_bal = user.get_balance()
    new_bal = user_bal - float(instance.amount_tf)
    user.account_balance = new_bal
    user.save()


post_save.connect(user_balance_signal, Transaction)