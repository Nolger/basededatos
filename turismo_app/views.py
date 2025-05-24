from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from datetime import datetime
from turismo_app.models import Client # Importar para validación

class AdvancedTourSummaryAPIView(APIView):
    def get(self, request):
        client_id = request.query_params.get('client_id')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        if not all([client_id, start_date_str, end_date_str]):
            return Response(
                {"error": "Los parámetros 'client_id', 'start_date' y 'end_date' son requeridos."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client_id = int(client_id)
            if not Client.objects.filter(id=client_id).exists():
                return Response(
                    {"error": f"Cliente con ID {client_id} no encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Formato de fecha inválido. Use YYYY-MM-DD. client_id debe ser un entero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Determinar el tipo de base de datos para la consulta SQL
        db_vendor = connection.vendor

        if db_vendor == 'postgresql':
            # Para PostgreSQL, usamos la función predefinida
            sql_query = "SELECT * FROM get_tour_summary(%s, %s, %s)"
            params = [client_id, start_date, end_date]
        elif db_vendor == 'mysql':
            sql_query = """
            SELECT
                tc.nombre AS client_name,
                tr.id AS tour_request_id,
                tr.fecha_tour AS tour_request_date,
                tp.nombre AS plan_name,
                tr.numero_personas AS num_people,
                tar.estado AS attention_status,
                tp.precio AS total_plan_price
            FROM
                turismo_app_tourrequest tr
            JOIN
                turismo_app_client tc ON tr.cliente_id = tc.id
            JOIN
                turismo_app_tourplan tp ON tr.plan_id = tp.id
            LEFT JOIN
                turismo_app_attentionrecord tar ON tr.id = tar.solicitud_id
            WHERE
                tc.id = %s AND
                tr.fecha_tour BETWEEN %s AND %s;
            """
            params = [client_id, start_date, end_date]
        elif db_vendor == 'microsoft': # Vendor para SQL Server en Django
            sql_query = """
            SELECT
                tc.nombre AS client_name,
                tr.id AS tour_request_id,
                tr.fecha_tour AS tour_request_date,
                tp.nombre AS plan_name,
                tr.numero_personas AS num_people,
                tar.estado AS attention_status,
                tp.precio AS total_plan_price
            FROM
                turismo_app_tourrequest tr
            JOIN
                turismo_app_client tc ON tr.cliente_id = tc.id
            JOIN
                turismo_app_tourplan tp ON tr.plan_id = tp.id
            LEFT JOIN
                turismo_app_attentionrecord tar ON tr.id = tar.solicitud_id
            WHERE
                tc.id = %s AND
                tr.fecha_tour BETWEEN %s AND %s;
            """
            # SQL Server usa '?' para los parámetros de pyodbc, pero Django ORM traduce '%s'
            # No obstante, si el driver directo tiene problemas, se puede ajustar a '?'
            params = [client_id, start_date, end_date]
        else:
            return Response(
                {"error": f"Base de datos no soportada para esta consulta: {db_vendor}"},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )

        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_query, params)
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                results = [dict(zip(columns, row)) for row in rows]

            except Exception as e:
                print(f"Error al ejecutar la consulta SQL en {db_vendor}: {e}")
                return Response(
                    {"error": f"Error en la base de datos al ejecutar la consulta: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(results, status=status.HTTP_200_OK)