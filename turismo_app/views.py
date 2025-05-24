from django.http import JsonResponse
from django.db import connection

def tour_summary_api(request):
    client_id = request.GET.get('client_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM tour_summary(%s, %s, %s)", [client_id, start_date, end_date])
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return JsonResponse(results, safe=False)
