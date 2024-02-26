from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import Token

from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Company, CompanyMember
from .serializers import CompanySerializer, CompanyMemberSerializer
from . import services
from rest_framework.test import APITestCase


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            company = services.create_company(
                serializer.validated_data['cnpj'],
                serializer.validated_data['corporate_name'],
                serializer.validated_data['trade_name'],
                owner_id=self.request.user.id,
            )
            output_serializer = CompanySerializer(company, context={'request': request})
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyMemberView(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        company_id = request.data.get('company')

        try:
            company_member = services.add_user_to_company(user_id, company_id)
            serializer = CompanyMemberSerializer(company_member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def get_companies(self, request):
        try:
            companies = services.get_companies(self.request.user.id)
            print(companies[0])
            serializer = CompanySerializer(companies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)

    def get_members(self, request):
        try:
            members = services.get_members(request.data['company_id'])
            serializer = UserSerializer(members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'message': e.message}, status=status.HTTP_400_BAD_REQUEST)


class CompanyViewSetTestCase(APITestCase):

    def setUp(self):
        # Create a user and set authentication
        self.user = User.objects.create_user(username='user', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.company_data = {
            'cnpj': '00.000.000/0001-00',
            'corporate_name': 'Test Company Ltd',
            'trade_name': 'TestCo',
        }

    def test_create_company(self):
        url = reverse('company-list')
        response = self.client.post(url, self.company_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().corporate_name, 'Test Company Ltd')


class CompanyMemberViewTestCase(APITestCase):

    def setUp(self):

        self.user_to_add = User.objects.create_user(username='newuser', password='password')
        self.company = Company.objects.create(
            cnpj='11.111.111/1111-11',
            corporate_name='Another Test Co',
            trade_name='AnotherTestCo',
            owner=self.user
        )

    def test_add_user_to_company(self):
        url = reverse('companymember-list')  # Adjust based on your URL conf
        data = {
            'user': self.user_to_add.id,
            'company': self.company.id,
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CompanyMember.objects.count(), 1)
        self.assertEqual(CompanyMember.objects.get().user, self.user_to_add)
