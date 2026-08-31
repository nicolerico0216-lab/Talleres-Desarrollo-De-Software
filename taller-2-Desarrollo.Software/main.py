

from datetime import datetime, timedelta

from modelos import SaldoInsuficienteError, CuentaBloqueadaError
from servicios import ClienteService, CuentaService, FacturaService, PagoService


def main():
    cliente_service = ClienteService()
    cuenta_service = CuentaService()
    factura_service = FacturaService()
    pago_service = PagoService()

     
    cliente = cliente_service.crear_cliente("Juan Pérez", "123456789", "juan@correo.com")
    print(f"Cliente creado: {cliente}")

   
    cuenta_ahorros = cuenta_service.crear_cuenta_ahorros("AH-001", 100000, cliente)
    cuenta_corriente = cuenta_service.crear_cuenta_corriente("CC-001", 20000, cliente, sobregiro=30000)
    print(f"Cuenta creada: {cuenta_ahorros}")
    print(f"Cuenta creada: {cuenta_corriente}")

    
    print("\n--- CU-02: Consultar saldo de cuenta ---")
    print(f"Saldo disponible cuenta de ahorros:   {cuenta_service.obtener_saldo_cuenta('AH-001', cliente)}")
    print(f"Saldo disponible cuenta corriente (incluye sobregiro): "
          f"{cuenta_service.obtener_saldo_cuenta('CC-001', cliente)}")

    factura = factura_service.crear_factura(cliente, 50000, datetime.now() + timedelta(days=15))
    print(f"\nFactura creada: {factura}")

    
    print("\n--- CU-01: Procesar pago (flujo principal) ---")
    pago = pago_service.procesar_pago(factura, cuenta_ahorros)
    print(f"Pago realizado: {pago}")
    print(f"Estado de la factura: {factura.estado}")
    print(f"Saldo restante en cuenta de ahorros: {cuenta_ahorros.saldo}")

    
    print("\n--- CU-01: Intentar pagar una factura ya pagada (excepción) ---")
    try:
        pago_service.procesar_pago(factura, cuenta_ahorros)
    except ValueError as error:
        print(f"Error controlado: {error}")

    
    print("\n--- CU-01: Procesar pago con saldo insuficiente (excepción) ---")
    factura_grande = factura_service.crear_factura(cliente, 999_999_999, datetime.now() + timedelta(days=15))
    try:
        pago_service.procesar_pago(factura_grande, cuenta_ahorros)
    except SaldoInsuficienteError as error:
        print(f"Error controlado: {error}")

    
    print("\n--- CU-01: Procesar pago con cuenta bloqueada (excepción) ---")
    cuenta_service.actualizar_cuenta("CC-001", estado="bloqueada")
    factura_2 = factura_service.crear_factura(cliente, 10000, datetime.now() + timedelta(days=10))
    try:
        pago_service.procesar_pago(factura_2, cuenta_corriente)
    except CuentaBloqueadaError as error:
        print(f"Error controlado: {error}")

   
    print("\n--- CU-03: Historial de pagos del cliente ---")
    for p in pago_service.obtener_pagos_por_cliente(cliente):
        print(p)

    
    print("\n--- CU-04: Facturas del cliente ---")
    for f in factura_service.obtener_facturas_por_cliente(cliente):
        print(f)


if __name__ == "__main__":
    main()

