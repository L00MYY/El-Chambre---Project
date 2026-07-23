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

## Cargar datos de demostración

El seed crea sucursales, productos, materias primas, inventarios, recetas,
una producción y ventas de ejemplo:

```bash
python scripts/seed_db.py
```

Si la base ya contiene información, el script no agrega duplicados. Para
reconstruirla y reemplazar su contenido por la demo:

```bash
python scripts/seed_db.py --reset
```
