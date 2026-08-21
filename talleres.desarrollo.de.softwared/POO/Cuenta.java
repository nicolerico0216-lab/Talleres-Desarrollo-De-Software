import java.math.BigDecimal;

public class Cuenta {

    private final String numero;
    private final String titular;
    private BigDecimal saldo;
    private BigDecimal limiteDescubierto;

   
    public Cuenta(String numero, String titular, BigDecimal saldoInicial) {

        if (saldoInicial.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException(
                "El saldo inicial no puede ser negativo"
            );
        }

        this.numero = numero;
        this.titular = titular;
        this.saldo = saldoInicial;
        this.limiteDescubierto = BigDecimal.ZERO;
    }

    
    public void depositar(BigDecimal monto) {

        if (monto.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException(
                "El monto debe ser positivo"
            );
        }

        this.saldo = this.saldo.add(monto);
    }

  
    public void debitar(BigDecimal monto) {

        if (monto.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException(
                "El monto debe ser positivo"
            );
        }

        BigDecimal saldoDisponible = this.saldo.add(limiteDescubierto);

        if (monto.compareTo(saldoDisponible) > 0) {
            throw new IllegalArgumentException(
                "Saldo insuficiente"
            );
        }

        this.saldo = this.saldo.subtract(monto);
    }

    public BigDecimal getSaldo() {
        return this.saldo;
    }

    
    public void setLimiteDescubierto(BigDecimal limiteDescubierto) {

        if (limiteDescubierto.compareTo(BigDecimal.ZERO) < 0) {
            throw new IllegalArgumentException(
                "El límite no puede ser negativo"
            );
        }

        this.limiteDescubierto = limiteDescubierto;
    }

   
    public String getNumero() {
        return numero;
    }

    public String getTitular() {
        return titular;
    }

    public BigDecimal getLimiteDescubierto() {
        return limiteDescubierto;
    }

    
    public static void main(String[] args) {

        Cuenta cuenta = new Cuenta(
            "001234",
            "María Paz",
            new BigDecimal("100000")
        );

        System.out.println("Cuenta: " + cuenta.getNumero());
        System.out.println("Titular: " + cuenta.getTitular());
        System.out.println("Saldo inicial: $" + cuenta.getSaldo());

        
        cuenta.depositar(new BigDecimal("50000"));

        System.out.println("Después del depósito: $"
                + cuenta.getSaldo());

        
        cuenta.setLimiteDescubierto(
            new BigDecimal("100000")
        );

       
        cuenta.debitar(new BigDecimal("200000"));

        System.out.println("Después del débito: $"
                + cuenta.getSaldo());

        System.out.println("Límite de descubierto: $"
                + cuenta.getLimiteDescubierto());
    }
}
