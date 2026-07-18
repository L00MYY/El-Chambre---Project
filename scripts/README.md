# Scripts

Carpeta para comandos auxiliares del proyecto.

Ejemplos esperados:

- `init_db.py`: crea la estructura de la base de datos local.
- `seed_db.py`: carga datos iniciales de prueba.
- `reset_db.py`: elimina los datos locales y reconstruye el esquema vacío.

Los scripts pueden importar código desde `src/`, pero no deben contener reglas de negocio.

## Reiniciar la base local

El comando solicita confirmación antes de eliminar el archivo SQLite configurado:

```bash
python scripts/reset_db.py
```

Para pruebas automatizadas o scripts puede omitirse la confirmación:

```bash
python scripts/reset_db.py --yes
```
