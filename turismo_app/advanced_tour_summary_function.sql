-- turismo_app/advanced_tour_summary_function.sql
-- Función para PostgreSQL

DROP FUNCTION IF EXISTS get_tour_summary(INTEGER, DATE, DATE);

CREATE OR REPLACE FUNCTION get_tour_summary(
    p_client_id INTEGER,
    p_start_date DATE,
    p_end_date DATE
)
RETURNS TABLE (
    client_name VARCHAR,
    tour_request_id INTEGER,
    tour_request_date DATE,
    plan_name VARCHAR,
    num_people INTEGER,
    attention_status VARCHAR,
    total_plan_price NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.nombre AS client_name,
        tr.id AS tour_request_id,
        tr.fecha_tour AS tour_request_date,
        tp.nombre AS plan_name,
        tr.numero_personas AS num_people,
        ar.estado AS attention_status,
        tp.precio AS total_plan_price
    FROM
        turismo_app_tourrequest tr
    JOIN
        turismo_app_client c ON tr.cliente_id = c.id
    JOIN
        turismo_app_tourplan tp ON tr.plan_id = tp.id
    LEFT JOIN
        turismo_app_attentionrecord ar ON tr.id = ar.solicitud_id
    WHERE
        c.id = p_client_id AND
        tr.fecha_tour BETWEEN p_start_date AND p_end_date;
END;
$$ LANGUAGE plpgsql;

-- Ejemplo de uso (ejecutar en pgAdmin o psql)
-- SELECT * FROM get_tour_summary(1, '2024-01-01', '2024-12-31');