from el_chambre.application.exceptions.exceptions import (
    ValidationError,
    NotFoundError,
)
from el_chambre.domain.entities.DetalleReceta import DetalleReceta


class RecetaService:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def guardar_receta(self, id_producto, ingredientes):
        if not ingredientes:
            raise ValidationError("La lista de ingredientes no puede estar vacía")

        with self._uow_factory() as uow:
            producto = uow.productos.get_by_id(id_producto)
            if producto is None:
                raise NotFoundError(f"El producto {id_producto} no existe")

            ids_vistos = set()
            detalles = []

            for ingrediente in ingredientes:
                id_materia = ingrediente["id_materia"]
                cantidad_usada = ingrediente["cantidad_usada"]

                if id_materia in ids_vistos:
                    raise ValidationError(
                        f"La materia prima {id_materia} está repetida en la receta"
                    )
                ids_vistos.add(id_materia)

                materia_prima = uow.materias_primas.get_by_id(id_materia)
                if materia_prima is None:
                    raise NotFoundError(f"La materia prima {id_materia} no existe")

                if cantidad_usada <= 0:
                    raise ValidationError(
                        f"La cantidad usada de la materia prima {id_materia} debe ser mayor que 0"
                    )

                detalles.append(
                    DetalleReceta(
                        idDetReceta=0,
                        idMateriaPrima=id_materia,
                        cantidadUsada=cantidad_usada,
                    )
                )

            uow.recetas.replace(id_producto, detalles)
            uow.commit()

            return detalles

    def obtener_receta(self, id_producto):
        with self._uow_factory() as uow:
            producto = uow.productos.get_by_id(id_producto)
            if producto is None:
                raise NotFoundError(f"El producto {id_producto} no existe")

            return uow.recetas.get_by_producto(id_producto)

    def eliminar_receta(self, id_producto):
        with self._uow_factory() as uow:
            producto = uow.productos.get_by_id(id_producto)
            if producto is None:
                raise NotFoundError(f"El producto {id_producto} no existe")

            receta_actual = uow.recetas.get_by_producto(id_producto)
            if not receta_actual:
                raise NotFoundError(
                    f"El producto {id_producto} no tiene una receta registrada"
                )

            uow.recetas.delete_by_producto(id_producto)
            uow.commit()