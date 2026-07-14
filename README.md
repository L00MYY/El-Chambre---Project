# El Chambre - Project

Aplicación demo para apoyar la gestión de inventario, ventas y producción de la panadería **El Chambre**.

El objetivo del proyecto es mantener una separación sencilla entre dominio, aplicación, infraestructura y futuras entradas externas como consola o API.

## Estructura del proyecto

```text
src/
└── el_chambre/
    ├── api/
    ├── application/
    ├── domain/
    └── infrastructure/

scripts/
docs/
tests/
```

## Carpetas principales

- `src/el_chambre/domain/`: entidades y reglas centrales del negocio.
- `src/el_chambre/application/`: servicios de aplicación y contratos de repositorios.
- `src/el_chambre/infrastructure/`: conexión a base de datos e implementación de repositorios.
- `src/el_chambre/api/`: espacio reservado para exponer funcionalidad mediante API.
- `scripts/`: comandos auxiliares, como carga inicial de datos.
- `docs/`: diagramas, notas de arquitectura y documentación de apoyo.
- `tests/`: pruebas y manuales de validación.

## Instalación

```bash
pip install -r requirements.txt
```

## Próximos pasos

1. Completar los métodos pendientes del dominio.
2. Implementar servicios de aplicación para ventas, inventario y producción.
3. Implementar repositorios SQLite.
4. Crear scripts para preparar y poblar la base de datos local.
5. Documentar pruebas manuales y comandos de uso.
