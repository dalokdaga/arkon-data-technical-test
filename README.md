# arkon-data-technical-test

Descripción corta del proyecto.

## Requisitos

- Python >= 3.9
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)

## Instalación Local Sin Docker

1. Clona el repositorio:

    ```bash
    git clone https://github.com/dalokdaga/arkon-data-technical-test
    ```

2. Instala las dependencias:

    ```bash
    cd arkon-data-technical-test
    pip install -r requirements.txt
    ```

## Configuración Local

1. Crea un archivo `.env` en la raíz del proyecto y configura las variables de entorno necesarias.

    ```
    TYPE_DB=mysql
    CONNECTION_URI=mysql+pymysql://user:password@localhost:3306/arkon_test
    SQLITE_DB_PATH=storage/database/database.db
    PATH_RULE_DB=config/db/drivers/rule_db.json
    FILE_NAME=puntos_de_acceso_wifi.csv
    FILE_PATH=storage/data_cdmx_wifi
    URL_BASE= "https://datos.cdmx.gob.mx/dataset/aa2ff336-b4aa-44f3-b38a-f303ef0f7673/resource/98f51fe2-18cb-4f50-a989-b9f81a2b5a76/download/{BASE_DATE}-puntos_de_acceso_wifi.csv"
    CELERY_BROKER_URL=redis://localhost:6379/0
    ```

## Uso

1. Ejecuta el servidor con Uvicorn:

    ```bash
    uvicorn config.app_run:app --reload
    ```

2. Accede a la documentación de la API en tu navegador web:

    ```
    http://localhost:8000/docs
    ```
1. Ejecuta Celery:

    ```bash
    celery -A config.celery worker      # Windows
    ```

    ```bash
    nohup celery -A config.celery worker --beat > celery.log 2>&1 &      # Linux
    ```

## Estructura del Proyecto

arkon-data-technical-test/
│
├───app/
│   ├───api/ : Estructura de API
│   │   ├───core/
│   │   │   ├───component/
│   │   │   │   ├───consult_access_component.py
│   │   │   │   └───__init__.py
│   │   │   ├───serializers/
│   │   │   │   ├───all_response.py
│   │   │   │   ├───id_response.py
│   │   │   │   └───process_data_serializer.py
│   │   │   ├───exceptions.py
│   │   │   ├───handler.py
│   │   │   ├───helper.py
│   │   │   ├───models.py
│   │   │   ├───paginator.py
│   │   │   ├───query_set.py
│   │   │   └───types.py
│   │   ├───v1/
│   │   │   ├───graphql/
│   │   │   │   └───wifi_access_schema.py
│   │   │   └───views.py
│   │   └───__init__.py
│   ├───core/ : Estructura para la ETL que prepara la data en la BD
│   │   ├───common/
│   │   │   ├───commands/
│   │   │   │   ├───console/
│   │   │   │   │   └───process_data_command.py
│   │   │   │   └───tasks/
│   │   │   │       └───process_data
│   │   │   └───utilities.py
│   │   ├───component/
│   │   │   ├───base_component.py
│   │   │   └───elt_data_wifi.py
│   │   └───exceptions.py
│   └───__init__.py
│
├───config/
│   ├───db/
│   │   ├───drivers/
│   │   │   ├───mysql/
│   │   │   │   ├───driver.py
│   │   │   │   └───__init__.py
│   │   │   ├───base_driver.py
│   │   │   └───rule_db.json
│   │   ├───conection_orm.py
│   │   ├───create_database.sql
│   │   └───factory_db.py
│   ├───app_run.py
│   ├───celery.py
│   ├───enviroment.py
│   ├───logging.py
│   └───__init__.py
│
├───diagrams/
│   ├───arquitectura_arkon.jpg
│   ├───Diagrama-DFD-LNL-0.jpg
│   ├───Diagrama-DFD-LNL-1.jpg
│   └───Diagrama-DFD-LNL-2.jpg
│
├───tests/
│   ├───__init__.py
│   └───test_api_handler.py
│
├───.gitignore
├───docker-compose.yml
├───Dockerfile
├───granphQL
├───pavement.py
├───README.md
└───requirements.txt

## Diagramas

### Arquitectura Arkon
![Arquitectura Arkon](diagrams/arquitectura_arkon.jpg)

### Diagrama de Flujo de Datos - Nivel 0
![Diagrama DFD LNL 0](diagrams/Diagrama-DFD-LNL-0.jpg)

### Diagrama de Flujo de Datos - Nivel 1
![Diagrama DFD LNL 1](diagrams/Diagrama-DFD-LNL-1.jpg)

### Diagrama de Flujo de Datos - Nivel 2
![Diagrama DFD LNL 2](diagrams/Diagrama-DFD-LNL-2.jpg)
