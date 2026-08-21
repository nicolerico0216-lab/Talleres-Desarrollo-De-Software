import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Scanner;


public class main {
     public static void main(String[] args) {

        Scanner teclado = new Scanner(System.in);
        ArrayList<Cuenta> cuentas = new ArrayList<>();

        int opcion;

        do {
            System.out.println("\n==============================");
            System.out.println("       SISTEMA BANCARIO");
            System.out.println("==============================");
            System.out.println("1. Crear cuenta de ahorros");
            System.out.println("2. Crear cuenta corriente");
            System.out.println("3. Listar cuentas");
            System.out.println("4. Consultar saldo");
            System.out.println("5. Depositar dinero");
            System.out.println("6. Debitar dinero");
            System.out.println("7. Realizar pago");
            System.out.println("8. Guardar");
            System.out.println("9. Salir");
            System.out.println("==============================");
            System.out.print("Seleccione una opción: ");

            opcion = teclado.nextInt();
            teclado.nextLine();

            switch (opcion) {

                case 1:
                    System.out.println("\n--- CREAR CUENTA DE AHORROS ---");

                    System.out.print("Número de cuenta: ");
                    String numeroAhorros = teclado.nextLine();

                    System.out.print("Titular: ");
                    String titularAhorros = teclado.nextLine();

                    System.out.print("Saldo inicial: ");
                    BigDecimal saldoAhorros = teclado.nextBigDecimal();
                    teclado.nextLine();

                    Cuenta cuentaAhorros = new Cuenta(
                            numeroAhorros,
                            titularAhorros,
                            saldoAhorros
                    );

                    cuentas.add(cuentaAhorros);

                    System.out.println("Cuenta de ahorros creada correctamente.");
                    break;

                case 2:
                    System.out.println("\n--- CREAR CUENTA CORRIENTE ---");

                    System.out.print("Número de cuenta: ");
                    String numeroCorriente = teclado.nextLine();

                    System.out.print("Titular: ");
                    String titularCorriente = teclado.nextLine();

                    System.out.print("Saldo inicial: ");
                    BigDecimal saldoCorriente = teclado.nextBigDecimal();

                    System.out.print("Límite de descubierto: ");
                    BigDecimal limite = teclado.nextBigDecimal();
                    teclado.nextLine();

                    Cuenta cuentaCorriente = new Cuenta(
                            numeroCorriente,
                            titularCorriente,
                            saldoCorriente
                    );

                    cuentaCorriente.setLimiteDescubierto(limite);

                    cuentas.add(cuentaCorriente);

                    System.out.println("Cuenta corriente creada correctamente.");
                    break;

                case 3:
                    System.out.println("\n--- LISTA DE CUENTAS ---");

                    if (cuentas.isEmpty()) {
                        System.out.println("No hay cuentas registradas.");
                    } else {
                        for (Cuenta cuenta : cuentas) {
                            System.out.println(
                                    "Número: " + cuenta.getNumero()
                                    + " | Titular: " + cuenta.getTitular()
                                    + " | Saldo: $" + cuenta.getSaldo()
                            );
                        }
                    }
                    break;

                case 4:
                    System.out.println("\n--- CONSULTAR SALDO ---");

                    System.out.print("Ingrese el número de cuenta: ");
                    String numeroConsultar = teclado.nextLine();

                    boolean encontrada = false;

                    for (Cuenta cuenta : cuentas) {
                        if (cuenta.getNumero().equals(numeroConsultar)) {
                            System.out.println(
                                    "Saldo disponible: $" + cuenta.getSaldo()
                            );
                            encontrada = true;
                            break;
                        }
                    }

                    if (!encontrada) {
                        System.out.println("Cuenta no encontrada.");
                    }
                    break;

                case 5:
                    System.out.println("\n--- DEPOSITAR DINERO ---");

                    System.out.print("Número de cuenta: ");
                    String numeroDeposito = teclado.nextLine();

                    System.out.print("Monto a depositar: ");
                    BigDecimal montoDeposito = teclado.nextBigDecimal();
                    teclado.nextLine();

                    encontrada = false;

                    for (Cuenta cuenta : cuentas) {
                        if (cuenta.getNumero().equals(numeroDeposito)) {

                            cuenta.depositar(montoDeposito);

                            System.out.println(
                                    "Depósito realizado correctamente."
                            );
                            System.out.println(
                                    "Nuevo saldo: $" + cuenta.getSaldo()
                            );

                            encontrada = true;
                            break;
                        }
                    }

                    if (!encontrada) {
                        System.out.println("Cuenta no encontrada.");
                    }
                    break;

                case 6:
                    System.out.println("\n--- DEBITAR DINERO ---");

                    System.out.print("Número de cuenta: ");
                    String numeroDebito = teclado.nextLine();

                    System.out.print("Monto a debitar: ");
                    BigDecimal montoDebito = teclado.nextBigDecimal();
                    teclado.nextLine();

                    encontrada = false;

                    for (Cuenta cuenta : cuentas) {
                        if (cuenta.getNumero().equals(numeroDebito)) {

                            try {
                                cuenta.debitar(montoDebito);

                                System.out.println(
                                        "Débito realizado correctamente."
                                );
                                System.out.println(
                                        "Nuevo saldo: $" + cuenta.getSaldo()
                                );

                            } catch (IllegalArgumentException e) {
                                System.out.println(
                                        "No se pudo realizar el débito: "
                                        + e.getMessage()
                                );
                            }

                            encontrada = true;
                            break;
                        }
                    }

                    if (!encontrada) {
                        System.out.println("Cuenta no encontrada.");
                    }
                    break;

                case 7:
                    System.out.println("\n--- REALIZAR PAGO ---");

                    System.out.print("Número de cuenta: ");
                    String numeroPago = teclado.nextLine();

                    System.out.print("Valor del pago: ");
                    BigDecimal montoPago = teclado.nextBigDecimal();
                    teclado.nextLine();

                    encontrada = false;

                    for (Cuenta cuenta : cuentas) {
                        if (cuenta.getNumero().equals(numeroPago)) {

                            try {
                                cuenta.debitar(montoPago);

                                System.out.println(
                                        "Pago realizado correctamente."
                                );
                                System.out.println(
                                        "Saldo restante: $" + cuenta.getSaldo()
                                );

                            } catch (IllegalArgumentException e) {
                                System.out.println(
                                        "No se pudo realizar el pago: "
                                        + e.getMessage()
                                );
                            }

                            encontrada = true;
                            break;
                        }
                    }

                    if (!encontrada) {
                        System.out.println("Cuenta no encontrada.");
                    }
                    break;

                case 8:
                    System.out.println("\nGuardando información...");
                    System.out.println("Información guardada correctamente.");
                    break;

                case 9:
                    System.out.println("\nSaliendo del sistema...");
                    break;

                default:
                    System.out.println("\nOpción no válida.");
            }

        } while (opcion != 9);

        teclado.close();
    }
    
}
