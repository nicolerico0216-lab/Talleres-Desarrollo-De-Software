
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
import uuid


class SaldoInsuficienteError(Exception):
   
    pass


class CuentaBloqueadaError(Exception):
    
    pass


class Cliente:
    

    def __init__(self, nombre: str, documento: str, email: str):
        self._id = str(uuid.uuid4())[:8]
        self._nombre = nombre
        self._documento = documento
        self._email = email
        self._cuentas: List["Cuenta"] = []
        self._facturas: List["Factura"] = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def documento(self) -> str:
        return self._documento

    @property
    def email(self) -> str:
        return self._email

    @property
    def cuentas(self) -> List["Cuenta"]:
        return self._cuentas

    @property
    def facturas(self) -> List["Factura"]:
        return self._facturas

    def agregar_cuenta(self, cuenta: "Cuenta") -> None:
        self._cuentas.append(cuenta)

    def agregar_factura(self, factura: "Factura") -> None:
        self._facturas.append(factura)

    def __str__(self) -> str:
        return f"Cliente(id={self._id}, nombre={self._nombre})"


class Cuenta(ABC):
    

    def __init__(self, numero_cuenta: str, saldo_inicial: float, titular: Cliente):
        self._numero_cuenta = numero_cuenta
        self._saldo = saldo_inicial
        self._titular = titular
        self._estado = "activa"  
        titular.agregar_cuenta(self)

    @property
    def numero_cuenta(self) -> str:
        return self._numero_cuenta

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def titular(self) -> Cliente:
        return self._titular

    def bloquear(self) -> None:
        self._estado = "bloqueada"

    def desbloquear(self) -> None:
        self._estado = "activa"

    def depositar(self, monto: float) -> None:
        if self._estado == "bloqueada":
            raise CuentaBloqueadaError("La cuenta se encuentra bloqueada")
        self._saldo += monto

    def retirar(self, monto: float) -> None:
        if self._estado == "bloqueada":
            raise CuentaBloqueadaError("La cuenta se encuentra bloqueada")
        if monto > self.calcular_saldo_disponible():
            raise SaldoInsuficienteError("Saldo insuficiente para procesar el pago")
        self._saldo -= monto

    @abstractmethod
    def calcular_saldo_disponible(self) -> float:
        
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(numero={self._numero_cuenta}, saldo={self._saldo})"


class CuentaAhorros(Cuenta):
    

    def __init__(self, numero_cuenta: str, saldo_inicial: float, titular: Cliente,
                 tasa_interes: float = 0.02):
        super().__init__(numero_cuenta, saldo_inicial, titular)
        self._tasa_interes = tasa_interes

    @property
    def tasa_interes(self) -> float:
        return self._tasa_interes

    def calcular_saldo_disponible(self) -> float:
       
        return self._saldo

    def aplicar_interes(self) -> None:
        self._saldo += self._saldo * self._tasa_interes


class CuentaCorriente(Cuenta):
    

    def __init__(self, numero_cuenta: str, saldo_inicial: float, titular: Cliente,
                 sobregiro_permitido: float = 50000):
        super().__init__(numero_cuenta, saldo_inicial, titular)
        self._sobregiro_permitido = sobregiro_permitido

    @property
    def sobregiro_permitido(self) -> float:
        return self._sobregiro_permitido

    def calcular_saldo_disponible(self) -> float:
       
        return self._saldo + self._sobregiro_permitido


class Factura:
    

    def __init__(self, cliente: Cliente, monto: float, fecha_vencimiento: datetime):
        self._id = str(uuid.uuid4())[:8]
        self._cliente = cliente
        self._monto = monto
        self._fecha_vencimiento = fecha_vencimiento
        self._estado = "pendiente"  
        cliente.agregar_factura(self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def fecha_vencimiento(self) -> datetime:
        return self._fecha_vencimiento

    @property
    def estado(self) -> str:
        return self._estado

    def marcar_como_pagada(self) -> None:
        self._estado = "pagada"

    def __str__(self) -> str:
        return f"Factura(id={self._id}, monto={self._monto}, estado={self._estado})"


class Pago:
    

    def __init__(self, factura: Factura, cuenta_origen: Cuenta, monto: float):
        self._id = str(uuid.uuid4())[:8]
        self._factura = factura
        self._cuenta_origen = cuenta_origen
        self._monto = monto
        self._fecha = datetime.now()
        self._estado = "pendiente"  

    @property
    def id(self) -> str:
        return self._id

    @property
    def factura(self) -> Factura:
        return self._factura

    @property
    def cuenta_origen(self) -> Cuenta:
        return self._cuenta_origen

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def estado(self) -> str:
        return self._estado

    def marcar_exitoso(self) -> None:
        self._estado = "exitoso"

    def marcar_fallido(self) -> None:
        self._estado = "fallido"

    def __str__(self) -> str:
        return f"Pago(id={self._id}, monto={self._monto}, estado={self._estado})"
