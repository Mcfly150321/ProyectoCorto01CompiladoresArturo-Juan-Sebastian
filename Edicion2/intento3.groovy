class ProcesadorVentas {
    double impuestoEstatal = 0.12
    int limiteEnvioGratis = 500

    def calcularTotal(double montoBase, int cantidadItems, boolean esClienteVIP) {
        double subtotal = montoBase * cantidadItems
        double descuento = 0.0

        if (esClienteVIP) {
            descuento = subtotal * 0.15
        } else if (subtotal >= 1000.0) {
            descuento = subtotal * 0.10
        }

        double totalConDescuento = subtotal - descuento
        double totalFinal = totalConDescuento + (totalConDescuento * impuestoEstatal)

        return totalFinal
    }
}

def procesador = new ProcesadorVentas()
double resultadoVenta = procesador.calcularTotal(150.0, 4, true)
