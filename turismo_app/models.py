from django.db import models
from django.core.validators import MinValueValidator

class Client(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    documento_identidad = models.CharField(max_length=50, unique=True)
    nacionalidad = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} ({self.documento_identidad})"

class TouristSite(models.Model):
    TIPO_SITIO_CHOICES = [
        ('natural', 'Natural'),
        ('cultural', 'Cultural'),
        ('aventura', 'Aventura'),
        ('historico', 'Histórico'),
        ('gastronomico', 'Gastronómico'),
        ('urbano', 'Urbano'),
    ]
    nombre = models.CharField(max_length=200, unique=True)
    ubicacion = models.CharField(max_length=255)
    tipo_sitio = models.CharField(max_length=50, choices=TIPO_SITIO_CHOICES)
    descripcion = models.TextField()

    class Meta:
        verbose_name = "Sitio Turístico"
        verbose_name_plural = "Sitios Turísticos"

    def __str__(self):
        return self.nombre

class TourPlan(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField()
    duracion_total = models.IntegerField(validators=[MinValueValidator(1)]) # en días
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sitios = models.ManyToManyField(TouristSite, through='PlanSiteDetail')

    class Meta:
        verbose_name = "Plan Turístico"
        verbose_name_plural = "Planes Turísticos"

    def __str__(self):
        return self.nombre

class PlanSiteDetail(models.Model):
    plan = models.ForeignKey(TourPlan, on_delete=models.CASCADE)
    sitio = models.ForeignKey(TouristSite, on_delete=models.CASCADE)
    orden_visita = models.IntegerField(validators=[MinValueValidator(1)])
    tiempo_estimado_horas = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.1)])

    class Meta:
        unique_together = (('plan', 'sitio'), ('plan', 'orden_visita'))
        verbose_name = "Detalle de Plan y Sitio"
        verbose_name_plural = "Detalles de Planes y Sitios"
        ordering = ['plan', 'orden_visita']

    def __str__(self):
        return f"Plan: {self.plan.nombre} - Sitio: {self.sitio.nombre} (Orden: {self.orden_visita})"

class TourRequest(models.Model):
    fecha_solicitud = models.DateField(auto_now_add=True)
    fecha_tour = models.DateField()
    numero_personas = models.IntegerField(validators=[MinValueValidator(1)])
    observaciones = models.TextField(blank=True, null=True)
    plan = models.ForeignKey(TourPlan, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Client, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Solicitud de Tour"
        verbose_name_plural = "Solicitudes de Tour"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Solicitud de {self.cliente.nombre} para {self.plan.nombre} el {self.fecha_tour}"

class AttentionRecord(models.Model):
    ESTADO_ATENCION_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
        ('realizado', 'Realizado'),
        ('reprogramado', 'Reprogramado'),
    ]
    solicitud = models.OneToOneField(TourRequest, on_delete=models.CASCADE, primary_key=True)
    estado = models.CharField(max_length=50, choices=ESTADO_ATENCION_CHOICES, default='pendiente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Registro de Atención"
        verbose_name_plural = "Registros de Atención"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"Atención para solicitud {self.solicitud.id} - Estado: {self.estado}"