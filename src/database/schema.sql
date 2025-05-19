-- Table: public.emprendedores

-- DROP TABLE IF EXISTS public.emprendedores;

CREATE TABLE IF NOT EXISTS public.emprendedores
(
    id integer NOT NULL DEFAULT nextval('emprendedores_id_seq'::regclass),
    nombre character varying(255) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default",
    edad integer,
    universidad character varying(255) COLLATE pg_catalog."default",
    carrera character varying(255) COLLATE pg_catalog."default",
    semestre character varying(50) COLLATE pg_catalog."default",
    experiencia_previa character varying(10) COLLATE pg_catalog."default",
    nombre_emprendimiento character varying(255) COLLATE pg_catalog."default",
    descripcion_emprendimiento text COLLATE pg_catalog."default",
    clasificaciones_niza jsonb,
    fecha_registro timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    acepta_politica boolean DEFAULT false,
    CONSTRAINT emprendedores_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.emprendedores
    OWNER to dcajiao;