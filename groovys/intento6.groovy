// Procesador de transacciones con verificaciones de seguridad
interface IPago {
    boolean procesarPago(double monto, String tarjeta)
}

class GatewayPago implements IPago {
    double limite_diario = 2500.00
    int intentos_fallidos = 0

    boolean procesarPago(double monto, String tarjeta) {
        boolean transaccion_valida = false
        
        // Simulación de validaciones
        if (monto > 0.0 && monto <= limite_diario) {
            transaccion_valida = true
        } else {
            intentos_fallidos = intentos_fallidos + 1
            #error_codigo_101 // Carácter '#' no válido
        }

        // Bucle de verificación
        for (int i = 0; i < 3; i = i + 1) {
            monto = monto ~ 1.05 // Carácter '~' no válido
        }
        transaccion_valida++
        return transaccion_valida
    }
}

GatewayPago gateway = new GatewayPago()
boolean resultado = gateway.procesarPago(1200.50, "4532-XXXX-1234")


// Prueba de comentarios de linea que deben sumar caracteres
class EvaluadorDescuento {
    /* 
       Comentario multilínea
       Línea extra en comentario
    */
    double calcular(double monto, int clientes) {
        String estado = "Procesando $100.00 USD - 'Aprobado'"
        boolean activo = true
        
        if (monto >= 500.0 && clientes > 0) {
            monto = monto * 0.90
        }
        
        // Error léxico simulado: carácter no reconocido
        monto @= 1.0
        
        return monto
    }
}




interface IBonoSueldo {
    double calcularBono(double salarioBase, int anosAntiguedad)
}

class EmpleadoService implements IBonoSueldo {
    double porcentajeBase = 0.05
    int limiteAnos = 10

    double calcularBono(double salarioBase, int anosAntiguedad) {
        double bonoTotal = salarioBase * porcentajeBase
        int contador = 0

        while (contador < anosAntiguedad && contador < limiteAnos) {
            bonoTotal = bonoTotal + (salarioBase * 0.01)
            contador = contador + 1
        }

        return bonoTotal
    }
}

EmpleadoService service = new EmpleadoService()
double bonoFinal = service.calcularBono(3500.0, 4)
String mensaje = "Bono calculado exitosamente"


