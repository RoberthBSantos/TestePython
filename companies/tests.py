from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import User, Company, CompanyMember
from .services import create_company, add_user_to_company, get_companies, get_members


class CreateCompanyTest(TestCase):

    def setUp(self):
        self.owner = User.objects.create(first_name='owner', email='owner@example.com')

    def test_create_company(self):
        cnpj = '00.000.000/0001-00'
        razao_social = 'Test Company Ltd'
        nome_fantasia = 'TestCo'
        owner_id = self.owner.id

        company = create_company(cnpj, razao_social, nome_fantasia, owner_id)

        self.assertIsNotNone(company.pk)
        self.assertEqual(company.corporate_name, razao_social)
        self.assertEqual(company.trade_name, nome_fantasia)
        self.assertEqual(company.owner, self.owner)


class AddUserToCompanyTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='user', email='user@example.com')
        self.owner = User.objects.create(first_name='owner', email='owner@example.com')
        self.company = Company.objects.create(cnpj='11.111.111/1111-11', corporate_name='TestCo Ltd',
                                              trade_name='TestCo', owner=self.owner)

    def test_add_user_to_company(self):
        company_member = add_user_to_company(self.user.id, self.company.id)

        self.assertIsNotNone(company_member.pk)
        self.assertEqual(company_member.user, self.user)
        self.assertEqual(company_member.company, self.company)

    def test_add_existing_user_raises_validation_error(self):
        add_user_to_company(self.user.id, self.company.id)

        with self.assertRaises(ValidationError):
            add_user_to_company(self.user.id, self.company.id)


class GetCompaniesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(first_name='user', email='user@example.com')
        self.company1 = Company.objects.create(cnpj='22.222.222/2222-22', corporate_name='Company One',
                                               trade_name='CompOne', owner=self.user)
        self.company2 = Company.objects.create(cnpj='33.333.333/3333-33', corporate_name='Company Two',
                                               trade_name='CompTwo', owner=self.user)
        CompanyMember.objects.create(user=self.user, company=self.company1)
        CompanyMember.objects.create(user=self.user, company=self.company2)

    def test_get_companies(self):
        companies = get_companies(self.user.id)

        self.assertEqual(len(companies), 2)
        self.assertIn(self.company1, companies)
        self.assertIn(self.company2, companies)


class GetMembersTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(first_name='user1', email='user1@example.com')
        self.user2 = User.objects.create(first_name='user2', email='user2@example.com')
        self.company = Company.objects.create(cnpj='44.444.444/4444-44', corporate_name='Company Members',
                                              trade_name='CompMembers', owner=self.user1)
        CompanyMember.objects.create(user=self.user1, company=self.company)
        CompanyMember.objects.create(user=self.user2, company=self.company)

    def test_get_members(self):
        members = get_members(self.company.id)

        self.assertEqual(len(members), 2)
        self.assertIn(self.user1, members)
        self.assertIn(self.user2, members)
