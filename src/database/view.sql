SELECT
    id,
    nombre,
    email,
    edad,
    universidad,
    carrera,
    semestre,
    experiencia_previa,
    nombre_emprendimiento,
    descripcion_emprendimiento,
    fecha_registro,
    acepta_politica,
    ((clasificaciones_niza -> 0) ->> 'clase' :: text) :: integer AS clase_1,
    (
        (clasificaciones_niza -> 0) ->> 'confianza' :: text
    ) :: integer AS confianza_1,
    (clasificaciones_niza -> 0) ->> 'relevancia' :: text AS relevancia_1,
    (clasificaciones_niza -> 0) ->> 'descripcion' :: text AS descripcion_1
FROM
    emprendedores;