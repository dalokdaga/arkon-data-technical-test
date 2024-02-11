SELECT
    rw.id,
    rw.programa,
    rw.fecha_instalacion,
    rw.latitud,
    rw.longitud,
    c.colonia,
    c.alcaldia,
    (6371 * acos(cos(radians(%s)) * cos(radians(rw.latitud)) *
    cos(radians(rw.longitud) - radians(%s)) +
    sin(radians(%s)) * sin(radians(rw.latitud)))) AS distancia
FROM
    arkon_test.registros_wifi rw
left join arkon_test.colonies c on
    rw.id_colonia = c.id
ORDER BY
    distancia