from rest_framework import serializers
from .models import Company, CompanyMember


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'owner', 'cnpj', 'corporate_name', 'trade_name')


class CompanyMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMember
        fields = ('user', 'company')
