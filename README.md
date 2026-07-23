# El Chambre

API local para administrar inventario, recetas, producción y ventas de una
panadería. Utiliza Python, Flask y SQLite.

## Requisitos

- Python 3.10 o superior
- Postman CLI, únicamente para ejecutar la colección

## Instalación

```powershell
git clone https://github.com/L00MYY/El-Chambre---Project.git
cd El-Chambre---Project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Base de datos

Crear una base vacía:

```powershell
python scripts\init_db.py
```

O reconstruirla con datos de demostración:

```powershell
python scripts\seed_db.py --reset
```

## Ejecutar la API

```powershell
$env:PYTHONPATH="$PWD\src"
python -m flask --app el_chambre.api.app run
```

La API estará disponible en `http://localhost:5000`.

## Colección Postman

```powershell
postman collection lint postman/collections/El-Chambre-API
postman collection run postman/collections/El-Chambre-API `
  -e postman/environments/Local.environment.yaml `
  --bail
```

La guía breve se encuentra en [`postman/README.md`](postman/README.md).

## Estructura

```text
src/el_chambre/   dominio, aplicación, infraestructura y API
scripts/          inicialización, reinicio y datos demo
postman/          colección ejecutable
docs/diagrams/    diagramas del proyecto
```
