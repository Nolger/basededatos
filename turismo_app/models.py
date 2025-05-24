from django.db import models

class Client(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documento_identidad = models.CharField(max_length=50, unique=True)
    nacionalidad = models.CharField(max_length=50)

    def __str__(self): return self.nombre

class TouristSite(models.Model):
    TIPO_CHOICES = [
        ('natural', 'Natural'),
        ('cultural', 'Cultural'),
        ('aventura', 'Aventura'),
    ]
    nombre = models.CharField(max_length=100, unique=True)
    ubicacion = models.CharField(max_length=100)
    tipo_sitio = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()

    def __str__(self): return self.nombre

class TourPlan(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    duracion_total = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    sitios = models.ManyToManyField(TouristSite, through='PlanSiteDetail')

    def __str__(self): return self.nombre

class PlanSiteDetail(models.Model):
    plan = models.ForeignKey(TourPlan, on_delete=models.CASCADE)
    sitio = models.ForeignKey(TouristSite, on_delete=models.CASCADE)
    orden_visita = models.IntegerField()
    tiempo_estimado_horas = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = [('plan', 'sitio'), ('plan', 'orden_visita')]

class TourRequest(models.Model):
    fecha_solicitud = models.DateField()
    fecha_tour = models.DateField()
    numero_personas = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    plan = models.ForeignKey(TourPlan, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)

class AttentionRecord(models.Model):
    ESTADO_CHOICES = [
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
    ]
    solicitud = models.OneToOneField(TourRequest, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField(blank=True, null=True)
