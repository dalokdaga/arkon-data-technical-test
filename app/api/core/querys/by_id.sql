SELECT 
    rw.id,
    rw.programa,
    rw.fecha_instalacion,
    rw.latitud,
    rw.longitud,
    c.colonia,
    c.alcaldia 
FROM arkon_test.registros_wifi rw 
left join arkon_test.colonies c on rw.id_colonia = c.id 
where rw.id = '%s'