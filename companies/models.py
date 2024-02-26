from django.db import models
from accounts.models import User


class Company(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_companies', null=True, blank=True)
    cnpj = models.CharField(max_length=20, unique=True)
    corporate_name = models.CharField(max_length=100)
    trade_name = models.CharField(max_length=100)

    def __str__(self):
        return self.trade_name


class CompanyMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return f"{self.user.email} - {self.company.trade_name}"
