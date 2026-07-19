from el_chambre.application.exceptions.exceptions import (
    NotFoundError,
    ValidationError,
)
from el_chambre.domain.entities.MateriaPrima import MateriaPrima
from el_chambre.domain.entities.Producto import Producto
from el_chambre.domain.entities.Sucursal import Sucursal


class CatalogoService:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    # Productos

    def crear_producto(self, nombre, precio, descripcion=""):
        nombre = self._validar_texto(nombre, "El nombre")
        precio = self._validar_numero_no_negativo(precio, "El precio")

        with self._uow_factory() as uow:
            producto = Producto(0, nombre, precio, descripcion or "", [])
            producto.idProducto = uow.productos.add(producto)
            uow.commit()
            return producto

    def obtener_producto(self, id_producto):
        with self._uow_factory() as uow:
            producto = uow.productos.get_by_id(id_producto)
            if producto is None:
                raise NotFoundError(f"El producto {id_producto} no existe")
            return producto

    def listar_productos(self):
        with self._uow_factory() as uow:
            return uow.productos.list_all()

    def actualizar_producto(self, id_producto, nombre, precio, descripcion=""):
        nombre = self._validar_texto(nombre, "El nombre")
        precio = self._validar_numero_no_negativo(precio, "El precio")

        with self._uow_factory() as uow:
            producto = uow.productos.get_by_id(id_producto)
            if producto is None:
                raise NotFoundError(f"El producto {id_producto} no existe")

            producto.nombre = nombre
            producto.precio = precio
            producto.descripcion = descripcion or ""
            uow.productos.update(producto)
            uow.commit()
            return producto

    # Materias primas

    def crear_materia_prima(
        self,
        nombre,
        unidad_medida,
        costo_unitario=0,
        descripcion="",
    ):
        nombre = self._validar_texto(nombre, "El nombre")
        unidad_medida = self._validar_texto(unidad_medida, "La unidad de medida")
        costo_unitario = self._validar_numero_no_negativo(
            costo_unitario,
            "El costo unitario",
        )

        with self._uow_factory() as uow:
            materia_prima = MateriaPrima(
                0,
                nombre,
                unidad_medida,
                costo_unitario,
                descripcion or "",
            )
            materia_prima.idMateriaPrima = uow.materias_primas.add(materia_prima)
            uow.commit()
            return materia_prima

    def obtener_materia_prima(self, id_materia):
        with self._uow_factory() as uow:
            materia_prima = uow.materias_primas.get_by_id(id_materia)
            if materia_prima is None:
                raise NotFoundError(f"La materia prima {id_materia} no existe")
            return materia_prima

    def listar_materias_primas(self):
        with self._uow_factory() as uow:
            return uow.materias_primas.list_all()

    def actualizar_materia_prima(
        self,
        id_materia,
        nombre,
        unidad_medida,
        costo_unitario=0,
        descripcion="",
    ):
        nombre = self._validar_texto(nombre, "El nombre")
        unidad_medida = self._validar_texto(unidad_medida, "La unidad de medida")
        costo_unitario = self._validar_numero_no_negativo(
            costo_unitario,
            "El costo unitario",
        )

        with self._uow_factory() as uow:
            materia_prima = uow.materias_primas.get_by_id(id_materia)
            if materia_prima is None:
                raise NotFoundError(f"La materia prima {id_materia} no existe")

            materia_prima.nombre = nombre
            materia_prima.unidadMedida = unidad_medida
            materia_prima.costoUnitario = costo_unitario
            materia_prima.descripcion = descripcion or ""
            uow.materias_primas.update(materia_prima)
            uow.commit()
            return materia_prima

    # Sucursales

    def crear_sucursal(self, nombre, direccion, telefono=None):
        nombre = self._validar_texto(nombre, "El nombre")
        direccion = self._validar_texto(direccion, "La dirección")

        with self._uow_factory() as uow:
            sucursal = Sucursal(0, nombre, direccion, telefono)
            sucursal._idSucursal = uow.sucursales.add(sucursal)
            uow.commit()
            return sucursal

    def obtener_sucursal(self, id_sucursal):
        with self._uow_factory() as uow:
            sucursal = uow.sucursales.get_by_id(id_sucursal)
            if sucursal is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")
            return sucursal

    def listar_sucursales(self):
        with self._uow_factory() as uow:
            return uow.sucursales.list_all()

    def actualizar_sucursal(self, id_sucursal, nombre, direccion, telefono=None):
        nombre = self._validar_texto(nombre, "El nombre")
        direccion = self._validar_texto(direccion, "La dirección")

        with self._uow_factory() as uow:
            sucursal = uow.sucursales.get_by_id(id_sucursal)
            if sucursal is None:
                raise NotFoundError(f"La sucursal {id_sucursal} no existe")

            sucursal._nombre = nombre
            sucursal._direccion = direccion
            sucursal._telefono = telefono
            uow.sucursales.update(sucursal)
            uow.commit()
            return sucursal

    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValidationError(f"{campo} es obligatorio")
        return valor.strip()

    @staticmethod
    def _validar_numero_no_negativo(valor, campo):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
            raise ValidationError(f"{campo} debe ser un número mayor o igual que 0")
        return valor
