# FernanBathroom

Aplicación web para centros educativos que permite llevar el control de los alumnos
que salen al baño durante las clases.

## Tecnologías

Python · Django · PostgreSQL · WhiteNoise

## Funcionalidades

- Registro de salidas al baño por alumno, con fecha y hora.
- Panel de administración para el profesorado.
- Indicación de necesidad médica en alumnos que lo requieran.

## Despliegue

Desplegada en https://fernan-bathroom.vercel.app

La configuración sensible se toma de variables de entorno: `DJANGO_SECRET_KEY`,
`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `ALLOWED_HOSTS` y `DEBUG`.

## Estado

Proyecto formativo, funcional y desplegado.
