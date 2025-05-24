CREATE OR REPLACE FUNCTION tour_summary(
    client_id_input INT,
    start_date_input DATE,
    end_date_input DATE
)
RETURNS TABLE (
    client_name TEXT,
    tour_request_id INT,
    tour_request_date DATE,
    plan_name TEXT,
    num_people INT,
    attention_status TEXT,
    total_plan_price NUMERIC
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.nombre,
        tr.id,
        tr.fecha_tour,
        tp.nombre,
        tr.numero_personas,
        ar.estado,
        tp.precio
    FROM turismo_app_tourrequest tr
    JOIN turismo_app_client c ON tr.cliente_id = c.id
    JOIN turismo_app_tourplan tp ON tr.plan_id = tp.id
    LEFT JOIN turismo_app_attentionrecord ar ON tr.id = ar.solicitud_id
    WHERE tr.cliente_id = client_id_input
      AND tr.fecha_tour BETWEEN start_date_input AND end_date_input;
END;
$$ LANGUAGE plpgsql;
