import random
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from faker import Faker
from turismo_app.models import Client, TouristSite, TourPlan, PlanSiteDetail, TourRequest, AttentionRecord
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populates the database with fake data for tourism app.'

    def add_arguments(self, parser):
        parser.add_argument('num_clients', type=int, help='Number of clients to create')
        parser.add_argument('num_sites', type=int, help='Number of tourist sites to create')
        parser.add_argument('num_plans', type=int, help='Number of tour plans to create')
        parser.add_argument('num_requests', type=int, help='Number of tour requests to create')

    def handle(self, *args, **options):
        fake = Faker('es_ES') # Usar localización en español

        num_clients = options['num_clients']
        num_sites = options['num_sites']
        num_plans = options['num_plans']
        num_requests = options['num_requests']

        self.stdout.write(self.style.WARNING("Clearing existing data..."))
        # Eliminar en orden inverso de dependencias para evitar errores de FK
        AttentionRecord.objects.all().delete()
        TourRequest.objects.all().delete()
        PlanSiteDetail.objects.all().delete()
        TourPlan.objects.all().delete()
        TouristSite.objects.all().delete()
        Client.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Existing data cleared."))


        self.stdout.write(self.style.SUCCESS(f"Creating {num_clients} clients..."))
        clients = []
        for _ in range(num_clients):
            try:
                client = Client.objects.create(
                    nombre=fake.name(),
                    correo=fake.unique.email(),
                    telefono=fake.phone_number() if random.random() > 0.3 else None,
                    documento_identidad=fake.unique.ssn(),
                    nacionalidad=fake.country(),
                )
                clients.append(client)
            except IntegrityError:
                continue # Skip if unique constraint violated (e.g., ssn/email collision from Faker)
        self.stdout.write(self.style.SUCCESS(f"Created {len(clients)} clients."))

        self.stdout.write(self.style.SUCCESS(f"Creating {num_sites} tourist sites..."))
        sites = []
        site_types = [choice[0] for choice in TouristSite.TIPO_SITIO_CHOICES]
        for _ in range(num_sites):
            try:
                site = TouristSite.objects.create(
                    nombre=fake.unique.city() + ' ' + fake.unique.street_name(),
                    ubicacion=fake.address(),
                    tipo_sitio=random.choice(site_types),
                    descripcion=fake.text(max_nb_chars=200),
                )
                sites.append(site)
            except IntegrityError:
                continue
        self.stdout.write(self.style.SUCCESS(f"Created {len(sites)} tourist sites."))

        self.stdout.write(self.style.SUCCESS(f"Creating {num_plans} tour plans..."))
        plans = []
        for _ in range(num_plans):
            try:
                plan = TourPlan.objects.create(
                    nombre=fake.unique.catch_phrase() + ' Tour',
                    descripcion=fake.text(max_nb_chars=300),
                    duracion_total=random.randint(1, 10),
                    precio=round(random.uniform(100.00, 2000.00), 2),
                )
                plans.append(plan)
            except IntegrityError:
                continue
        self.stdout.write(self.style.SUCCESS(f"Created {len(plans)} tour plans."))

        self.stdout.write(self.style.SUCCESS("Creating PlanSiteDetails..."))
        if not plans or not sites:
            self.stdout.write(self.style.WARNING("Not enough plans or sites to create PlanSiteDetails."))
        else:
            for plan in plans:
                num_sites_for_plan = random.randint(1, min(5, len(sites)))
                selected_sites = random.sample(sites, num_sites_for_plan)
                for order, site in enumerate(selected_sites, 1):
                    try:
                        PlanSiteDetail.objects.create(
                            plan=plan,
                            sitio=site,
                            orden_visita=order,
                            tiempo_estimado_horas=round(random.uniform(1.0, 8.0), 2),
                        )
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(f"Skipping duplicate PlanSiteDetail for {plan.nombre} and {site.nombre}"))
                        continue
            self.stdout.write(self.style.SUCCESS("PlanSiteDetails created."))

        self.stdout.write(self.style.SUCCESS(f"Creating {num_requests} tour requests and attention records..."))
        if not clients or not plans:
            self.stdout.write(self.style.WARNING("Not enough clients or plans to create TourRequests."))
        else:
            attention_statuses = [choice[0] for choice in AttentionRecord.ESTADO_ATENCION_CHOICES]
            for _ in range(num_requests):
                client = random.choice(clients)
                plan = random.choice(plans)
                
                # Ensure fecha_tour is in the future
                start_date = date.today() + timedelta(days=random.randint(1, 30))
                end_date = start_date + timedelta(days=plan.duracion_total)
                
                try:
                    tour_request = TourRequest.objects.create(
                        cliente=client,
                        plan=plan,
                        fecha_tour=start_date,
                        numero_personas=random.randint(1, 8),
                        observaciones=fake.sentence() if random.random() > 0.5 else None,
                    )
                    
                    # Create an AttentionRecord for each TourRequest
                    AttentionRecord.objects.create(
                        solicitud=tour_request,
                        estado=random.choice(attention_statuses),
                        comentarios=fake.text(max_nb_chars=100) if random.random() > 0.3 else None,
                    )
                except IntegrityError as e:
                    self.stdout.write(self.style.WARNING(f"Skipping TourRequest/AttentionRecord due to integrity error: {e}"))
                    continue
            self.stdout.write(self.style.SUCCESS(f"Created {num_requests} tour requests and attention records."))

        self.stdout.write(self.style.SUCCESS("Fake data generation complete!"))