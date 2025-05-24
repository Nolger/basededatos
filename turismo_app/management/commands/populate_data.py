from django.core.management.base import BaseCommand
from turismo_app.models import *
from faker import Faker
import random
from datetime import timedelta, date

fake = Faker()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sites = [TouristSite.objects.create(
            nombre=fake.unique.city(),
            ubicacion=fake.address(),
            tipo_sitio=random.choice(['natural', 'cultural', 'aventura']),
            descripcion=fake.text()
        ) for _ in range(10)]

        plans = []
        for _ in range(5):
            plan = TourPlan.objects.create(
                nombre=fake.unique.catch_phrase(),
                descripcion=fake.text(),
                duracion_total=random.randint(1, 10),
                precio=round(random.uniform(100.0, 1000.0), 2)
            )
            selected_sites = random.sample(sites, 3)
            for i, site in enumerate(selected_sites):
                PlanSiteDetail.objects.create(
                    plan=plan,
                    sitio=site,
                    orden_visita=i+1,
                    tiempo_estimado_horas=round(random.uniform(1.0, 5.0), 2)
                )
            plans.append(plan)

        for _ in range(20):
            client = Client.objects.create(
                nombre=fake.name(),
                correo=fake.unique.email(),
                telefono=fake.phone_number(),
                documento_identidad=fake.unique.ssn(),
                nacionalidad=fake.country()
            )
            for _ in range(random.randint(1, 3)):
                fecha_tour = fake.date_between(start_date='-30d', end_date='+30d')
                request = TourRequest.objects.create(
                    fecha_solicitud=fecha_tour - timedelta(days=random.randint(1, 10)),
                    fecha_tour=fecha_tour,
                    numero_personas=random.randint(1, 5),
                    observaciones=fake.text(),
                    plan=random.choice(plans),
                    cliente=client
                )
                AttentionRecord.objects.create(
                    solicitud=request,
                    estado=random.choice(['confirmado', 'cancelado', 'realizado']),
                    comentarios=fake.text()
                )
