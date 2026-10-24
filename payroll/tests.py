from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Employee, Payroll


class EmployeeNavigationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='employee', password='test-password')
        self.employee = Employee.objects.create(
            user=self.user,
            designation='Analyst',
            basic_salary=Decimal('50000.00'),
        )
        self.payroll = Payroll.objects.create(
            employee=self.employee,
            month='2026-10',
            basic_salary=Decimal('50000.00'),
        )
        self.client.login(username='employee', password='test-password')

    def test_dashboard_sidebar_links(self):
        response = self.client.get(reverse('dashboard'))

        self.assertContains(response, 'href="/#attendance"')
        self.assertContains(response, 'href="/#payroll">View Payslip</a>')
        self.assertContains(response, f'href="{reverse("profile")}">Profile</a>')
        self.assertContains(response, f'href="{reverse("settings")}">Settings</a>')

    def test_payslip_sidebar_links(self):
        response = self.client.get(reverse('payslip', args=[self.payroll.pk]))

        self.assertContains(response, 'href="/#payroll" class="active">View Payslip</a>')
        self.assertContains(response, f'href="{reverse("profile")}">Profile</a>')
        self.assertContains(response, f'href="{reverse("settings")}">Settings</a>')

    def test_profile_and_settings_pages_render(self):
        self.assertEqual(self.client.get(reverse('profile')).status_code, 200)
        self.assertEqual(self.client.get(reverse('settings')).status_code, 200)
