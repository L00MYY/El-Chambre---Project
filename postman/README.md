# Postman

Colección ejecutable de los 31 endpoints de El Chambre.

## Ejecutar

Preparar una base vacía:

```powershell
python scripts\reset_db.py --yes
```

Iniciar Flask:

```powershell
$env:PYTHONPATH="$PWD\src"
python -m flask --app el_chambre.api.app run
```

En otra terminal:

```powershell
postman collection run postman/collections/El-Chambre-API `
  -e postman/environments/Local.environment.yaml `
  --bail
```

Los archivos `*.request.yaml` contienen las solicitudes y pruebas. La colección
crea sus datos y guarda los identificadores en el ambiente local.

Las solicitudes representativas incluyen un ejemplo `Demo` con datos y respuesta
precargados para abrirlo y ejecutarlo desde Postman.
