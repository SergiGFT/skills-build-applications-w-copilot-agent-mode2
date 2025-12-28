
from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'


    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
        # Limpiar colecciones usando pymongo para evitar errores Djongo
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        for collection in ['leaderboard', 'activity', 'workout', 'user', 'team']:
            db[collection].delete_many({})
        client.close()

        self.stdout.write(self.style.SUCCESS('Creando equipos...'))
        marvel = Team.objects.create(name='Marvel', universe='Marvel')
        dc = Team.objects.create(name='DC', universe='DC')

        self.stdout.write(self.style.SUCCESS('Creando usuarios...'))
        users = [
            User.objects.create(email='tony@stark.com', name='Iron Man', team=marvel),
            User.objects.create(email='steve@rogers.com', name='Captain America', team=marvel),
            User.objects.create(email='bruce@wayne.com', name='Batman', team=dc),
            User.objects.create(email='clark@kent.com', name='Superman', team=dc),
        ]

        self.stdout.write(self.style.SUCCESS('Creando actividades...'))
        Activity.objects.create(user=users[0], type='Correr', duration=30, date=timezone.now())
        Activity.objects.create(user=users[1], type='Nadar', duration=45, date=timezone.now())
        Activity.objects.create(user=users[2], type='Bicicleta', duration=60, date=timezone.now())
        Activity.objects.create(user=users[3], type='Yoga', duration=20, date=timezone.now())

        self.stdout.write(self.style.SUCCESS('Creando workouts...'))
        w1 = Workout.objects.create(name='Entrenamiento Marvel', description='Rutina para héroes Marvel')
        w1.suggested_for.add(marvel)
        w2 = Workout.objects.create(name='Entrenamiento DC', description='Rutina para héroes DC')
        w2.suggested_for.add(dc)

        self.stdout.write(self.style.SUCCESS('Creando leaderboard...'))
        Leaderboard.objects.create(team=marvel, points=100, week=1)
        Leaderboard.objects.create(team=dc, points=80, week=1)

        self.stdout.write(self.style.SUCCESS('¡Base de datos poblada con datos de prueba!'))