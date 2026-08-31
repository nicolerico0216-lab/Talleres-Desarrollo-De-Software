

from datetime import datetime
from typing import Dict, List, Optional

from modelos import (
    Cliente,
    Cuenta,
    CuentaAhorros,
    CuentaCorriente,
    Factura,
    Pago,
    SaldoInsuficienteError,
    CuentaBloqueadaError,
)


class ClienteService:
    

    def __init__(self):
        self._clientes: Dict[str, Cliente] = {}

    def crear_cliente(self, nombre: str, documento: str, email: str) -> Cliente:
        cliente = Cliente(nombre, documento, email)
        self._clientes[cliente.id] = cliente
        return cliente

    def obtener_cliente(self, id_cliente: str) -> Optional[Cliente]:
        return self._clientes.get(id_cliente)

    def actualizar_cliente(self, id_cliente: str, nombre: Optional[str] = None,
                            email: Optional[str] = None) -> Optional[Cliente]:
        cliente = self._clientes.get(id_cliente)
        if not cliente:
            return None
        if nombre:
            cliente._nombre = nombre
        if email:
            cliente._email = email
        return cliente

    def eliminar_cliente(self, id_cliente: str) -> bool:
        return self._clientes.pop(id_cliente, None) is not None

    def listar_clientes(self) -> List[Cliente]:
        return list(self._clientes.values())


class CuentaService:
    

    def __init__(self):
        self._cuentas: Dict[str, Cuenta] = {}

    def crear_cuenta_ahorros(self, numero_cuenta: str, saldo_inicial: float,
                              titular: Cliente, tasa_interes: float = 0.02) -> CuentaAhorros:
        cuenta = CuentaAhorros(numero_cuenta, saldo_inicial, titular, tasa_interes)
        self._cuentas[numero_cuenta] = cuenta
        return cuenta

    def crear_cuenta_corriente(self, numero_cuenta: str, saldo_inicial: float,
                                titular: Cliente, sobregiro: float = 50000) -> CuentaCorriente:
        cuenta = CuentaCorriente(numero_cuenta, saldo_inicial, titular, sobregiro)
        self._cuentas[numero_cuenta] = cuenta
        return cuenta

    def obtener_cuenta(self, numero_cuenta: str) -> Optional[Cuenta]:
        return self._cuentas.get(numero_cuenta)

    def actualizar_cuenta(self, numero_cuenta: str, estado: Optional[str] = None) -> Optional[Cuenta]:
        cuenta = self._cuentas.get(numero_cuenta)
        if not cuenta:
            return None
        if estado == "bloqueada":
            cuenta.bloquear()
        elif estado == "activa":
            cuenta.desbloquear()
        return cuenta

    def eliminar_cuenta(self, numero_cuenta: str) -> bool:
        return self._cuentas.pop(numero_cuenta, None) is not None

    def obtener_saldo_cuenta(self, numero_cuenta: str, cliente_solicitante: Cliente) -> float:
      
        cuenta = self._cuentas.get(numero_cuenta)
        if cuenta is None:
            raise ValueError("Cuenta no encontrada")
        if cuenta.titular.id != cliente_solicitante.id:
            raise PermissionError("No tiene permisos para consultar esta cuenta")
        if cuenta.estado == "bloqueada":
            raise CuentaBloqueadaError("La cuenta se encuentra bloqueada")
       
        return cuenta.calcular_saldo_disponible()


class FacturaService:
    

    def __init__(self):
        self._facturas: Dict[str, Factura] = {}

    def crear_factura(self, cliente: Cliente, monto: float, fecha_vencimiento: datetime) -> Factura:
        factura = Factura(cliente, monto, fecha_vencimiento)
        self._facturas[factura.id] = factura
        return factura

    def obtener_factura(self, id_factura: str) -> Optional[Factura]:
        return self._facturas.get(id_factura)

    def actualizar_factura(self, id_factura: str, estado: Optional[str] = None) -> Optional[Factura]:
        factura = self._facturas.get(id_factura)
        if not factura:
            return None
        if estado == "pagada":
            factura.marcar_como_pagada()
        return factura

    def eliminar_factura(self, id_factura: str) -> bool:
        return self._facturas.pop(id_factura, None) is not None

    def obtener_facturas_por_cliente(self, cliente: Cliente,
                                      estado: Optional[str] = None) -> List[Factura]:
        
        facturas = [f for f in self._facturas.values() if f.cliente.id == cliente.id]
        if estado:
            facturas = [f for f in facturas if f.estado == estado]
        return facturas


class PagoService:
    

    def __init__(self):
        self._pagos: Dict[str, Pago] = {}

    def procesar_pago(self, factura: Factura, cuenta_origen: Cuenta) -> Pago:
       
        if factura.estado == "pagada":
            raise ValueError("La factura ya se encuentra pagada")

        pago = Pago(factura, cuenta_origen, factura.monto)
        self._pagos[pago.id] = pago

        try:
            cuenta_origen.retirar(factura.monto)  
            factura.marcar_como_pagada()
            pago.marcar_exitoso()
        except (SaldoInsuficienteError, CuentaBloqueadaError) as error:
            pago.marcar_fallido()
            raise error

        return pago

    def obtener_pago(self, id_pago: str) -> Optional[Pago]:
        return self._pagos.get(id_pago)

    def actualizar_pago(self, id_pago: str, estado: Optional[str] = None) -> Optional[Pago]:
        pago = self._pagos.get(id_pago)
        if not pago:
            return None
        if estado == "exitoso":
            pago.marcar_exitoso()
        elif estado == "fallido":
            pago.marcar_fallido()
        return pago

    def eliminar_pago(self, id_pago: str) -> bool:
        return self._pagos.pop(id_pago, None) is not None

    def obtener_pagos_por_cliente(self, cliente: Cliente) -> List[Pago]:
       
        pagos_cliente = [p for p in self._pagos.values() if p.cuenta_origen.titular.id == cliente.id]
        return sorted(pagos_cliente, key=lambda p: p.fecha, reverse=True)

