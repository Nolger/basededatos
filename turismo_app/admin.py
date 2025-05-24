from django.contrib import admin
from .models import Client, TouristSite, TourPlan, PlanSiteDetail, TourRequest, AttentionRecord

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'documento_identidad', 'nacionalidad', 'telefono')
    search_fields = ('nombre', 'correo', 'documento_identidad')
    list_filter = ('nacionalidad',)

@admin.register(TouristSite)
class TouristSiteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'tipo_sitio')
    search_fields = ('nombre', 'ubicacion', 'descripcion')
    list_filter = ('tipo_sitio',)

class PlanSiteDetailInline(admin.TabularInline):
    model = PlanSiteDetail
    extra = 1
    verbose_name = "Detalle del Sitio"
    verbose_name_plural = "Detalles de Sitios en el Plan"

@admin.register(TourPlan)
class TourPlanAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_total', 'precio')
    search_fields = ('nombre', 'descripcion')
    inlines = [PlanSiteDetailInline]

class AttentionRecordInline(admin.StackedInline):
    model = AttentionRecord
    can_delete = False
    verbose_name = "Registro de Atención"
    verbose_name_plural = "Registro de Atención"
    fieldsets = (
        (None, {
            'fields': ('estado', 'comentarios'),
        }),
    )

@admin.register(TourRequest)
class TourRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'plan', 'fecha_tour', 'numero_personas', 'fecha_solicitud')
    search_fields = ('cliente__nombre', 'plan__nombre', 'observaciones')
    list_filter = ('fecha_solicitud', 'fecha_tour', 'plan__nombre')
    inlines = [AttentionRecordInline]
    raw_id_fields = ('cliente', 'plan') # Útil para buscar clientes y planes en el admin

# PlanSiteDetail no necesita un admin propio si se maneja sólo como inline
# admin.site.register(PlanSiteDetail)

# AttentionRecord no necesita un admin propio si se maneja sólo como inline
# admin.site.register(AttentionRecord)