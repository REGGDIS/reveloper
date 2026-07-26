# Reveloper

Proyecto Django para la gestión de desarrollo y proyectos.

## Configuración del Entorno de Desarrollo Local

### 1. Creación del entorno virtual

```bash
python -m venv venv
```

Activar el entorno virtual:
- En Windows (PowerShell):
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- En Windows (CMD):
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- En Linux / macOS:
  ```bash
  source venv/bin/activate
  ```

### 2. Instalación de dependencias

```bash
pip install -r requirements.txt
```

### 3. Configuración de Variables de Entorno

Copiar la plantilla de variables de entorno:

- En Windows (PowerShell):
  ```powershell
  Copy-Item .env.example .env
  ```
- En Linux / macOS:
  ```bash
  cp .env.example .env
  ```

Editar el archivo `.env` configurando los valores requeridos para tu entorno local:

- **`DJANGO_SECRET_KEY`**: Clave secreta de Django (requerida).
- **`DJANGO_DEBUG`**: Modo depuración (`True` o `False`).
- **`DJANGO_ALLOWED_HOSTS`**: Hosts permitidos separados por comas (ej. `localhost,127.0.0.1`).
- **`DB_NAME`**: Nombre de la base de datos MySQL (ej. `reveloper`).
- **`DB_USER`**: Usuario de la base de datos MySQL (ej. `root`).
- **`DB_PASSWORD`**: Contraseña de la base de datos MySQL.
- **`DB_HOST`**: Host de la base de datos MySQL (ej. `localhost`).
- **`DB_PORT`**: Puerto de la base de datos MySQL (ej. `3306`).

### 4. Migraciones de Base de Datos

Aplicar las migraciones a la base de datos MySQL local:

```bash
python manage.py migrate
```

### 5. Ejecución del Servidor Local

```bash
python manage.py runserver
```

### 6. Ejecución de Pruebas Automatizadas

Para ejecutar las pruebas en un entorno aislado con SQLite en memoria:

```bash
python manage.py test Reveloper --settings=ProyectEspecial.test_settings
```
