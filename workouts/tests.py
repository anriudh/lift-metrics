from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Workout, Exercise
from datetime import date


class DashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.exercise = Exercise.objects.create(name='Bench Press', muscle_group='Chest', equipment='Barbell')
        
    def test_dashboard_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_dashboard_accessible_if_logged_in(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'workouts/dashboard.html')

    def test_dashboard_shows_recent_workouts(self):
        self.client.login(username='testuser', password='password123')
        # Create 6 workouts, should only see 5
        for i in range(6):
            Workout.objects.create(
                user=self.user,
                exercise=self.exercise,
                sets=3,
                reps=10,
                weight=100.00,
                date=date(2026, 3, 20 + i)
            )
        
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(len(response.context['recent_workouts']), 5)
        # Check order (most recent first)
        workouts = response.context['recent_workouts']
        self.assertEqual(workouts[0].date, date(2026, 3, 25))
        self.assertEqual(workouts[4].date, date(2026, 3, 21))
