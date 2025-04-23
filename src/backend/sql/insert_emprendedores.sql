INSERT INTO
    emprendedores (
        nombre,
        email,
        edad,
        universidad,
        carrera,
        semestre,
        experiencia_previa,
        nombre_emprendimiento,
        descripcion_emprendimiento,
        clasificaciones_niza,
        acepta_politica
    )
VALUES
    (
        :nombre,
        :email,
        :edad,
        :universidad,
        :carrera,
        :semestre,
        :experiencia_previa,
        :nombre_emprendimiento,
        :descripcion_emprendimiento,
        :clasificaciones_niza,
        :acepta_politica
    );