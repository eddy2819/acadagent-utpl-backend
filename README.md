# AcadAgent-UTPL

Backend para la homologación de asignaturas y la validación de propuestas TIC.

## Requisitos

- Docker Desktop con el motor en ejecución.
- Un archivo `.env` en la raíz, configurado a partir de `.env.example`.

## Arranque

```powershell
docker compose up -d --build
```

## Servicios locales

| Servicio | Dirección |
|---|---|
| API interactiva | http://localhost:8000/docs |
| Salud de la API | http://localhost:8000/api/v1/health |
| pgAdmin | http://localhost:5050 |
| PostgreSQL desde Windows | localhost:5433 |
| Consola de MinIO | http://localhost:9001 |
| Estado de ChromaDB | http://localhost:8001/api/v2/heartbeat |
| Modelos de Ollama | http://localhost:11434/api/tags |

## Preparación inicial

1. En la consola de MinIO, crear el bucket indicado en `MINIO_BUCKET`.
2. En pgAdmin, registrar PostgreSQL con host `postgres`, puerto `5432`
   y las credenciales `POSTGRES_*` del entorno.
3. Descargar y comprobar los modelos locales.

```powershell
docker compose exec backend python -m scripts.download_models
```

## Verificación

```powershell
docker compose exec backend python -m pytest -q
docker compose exec backend python -m scripts.check_services
```

## Uso diario

```powershell
docker compose up -d
docker compose stop
```
# acadagent-utpl-backend
