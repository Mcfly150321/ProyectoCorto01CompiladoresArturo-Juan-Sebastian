// Archivo de prueba extenso en Groovy (más de 75 líneas)
// Diseñado para evaluar contadores, palabras reservadas, flotantes, enteros, identificadores y operadores.

package com.analizador.pruebas

import java.util.logging.Logger
import java.time.LocalDate

@Slf4j
class SimuladorInventarioSistema {

    // Variables de configuración global
    public static final String VERSION_SISTEMA = "4.2.0"
    protected boolean modoDepuracion = true
    private double factorImpuestoLocal = 0.12
    
    // Contadores e índices
    int intentosConexionMaximos = 5
    long codigoTransaccionBase = 987654321L
    
    // Constructor principal
    public SimuladorInventarioSistema() {
        println("Inicializando Simulador de Inventario v${VERSION_SISTEMA}")
    }

    // Método para calcular el precio total con múltiples condiciones y tipos de datos
    def calcularCostoTotalInventario(List<Map> listaProductos, boolean aplicarDescuentoEspecial) {
        double acumuladorTotal = 0.0
        int cantidadProductosProcesados = 0
        
        // Bucle iterativo con validaciones lógicas y matemáticas
        for (int i = 0; i < listaProductos.size(); i++) {
            Map productoActual = listaProductos[i]
            
            double precioBase = productoActual.get("precio", 0.0)
            int stockDisponible = productoActual.get("stock", 0)
            
            if (stockDisponible > 0 && precioBase > 0.0) {
                double subtotalItem = precioBase * stockDisponible
                
                // Aplicar lógica de operador ternario y Elvis
                double descuento = aplicarDescuentoEspecial ? (subtotalItem * 0.15) : 0.0
                double costoNeto = subtotalItem - descuento
                
                acumuladorTotal += costoNeto
                cantidadProductosProcesados++
            } else {
                println("Advertencia: El producto ${productoActual.nombre} no tiene stock o precio válido.")
            }
        }
        
        // Retorno condicional usando flotantes y operaciones aritméticas avanzadas
        if (cantidadProductosProcesados >= 10) {
            return acumuladorTotal * (1.0 + this.factorImpuestoLocal)
        } else {
            return acumuladorTotal * 1.05
        }
    }

    // Método auxiliar para gestionar reportes de estado
    String generarReporteEstado(String usuarioResponsable) {
        LocalDate fechaActual = LocalDate.now()
        boolean estadoServidorActivo = true
        
        if (estadoServidorActivo && usuarioResponsable != null) {
            return "Reporte generado exitosamente por ${usuarioResponsable} en la fecha ${fechaActual}."
        } else {
            throw new IllegalArgumentException("Error crítico: Usuario no autorizado o servidor inactivo.")
        }
    }
    
    // Método estático para pruebas de expresiones regulares y operadores de Groovy
    static void validarPatronesYOperadores() {
        String textoPrueba = "Desarrollo de Compiladores 2026"
        
        // Uso de operadores de regex propios de Groovy (=~ y ==~)
        boolean coincideConDigitos = textoPrueba ==~ /.*2026.*/
        
        if (coincideConDigitos) {
            println("El texto coincide exactamente con el patrón de año buscado.")
        } else {
            println("No se encontró coincidencia exacta.")
        }
    }
}

// Bloque de ejecución principal (Script wrapper)
def ejecutarSimulacionCompleta() {
    SimuladorInventarioSistema simulador = new SimuladorInventarioSistema()
    
    List<Map> inventarioPrueba = [
        [nombre: "Laptop Gamer", precio: 2500.50, stock: 4],
        [nombre: "Mouse Inalámbrico", precio: 45.99, stock: 15],
        [nombre: "Teclado Mecánico", precio: 120.00, stock: 8]
    ]

    boolean banderaDescuento = true
    double resultadoFinal = simulador.calcularCostoTotalInventario(inventarioPrueba, banderaDescuento)
    
    println("El costo total calculado del inventario es: ${resultadoFinal}")
    
    String mensajeRespuesta = simulador.generarReporteEstado("Sebastian_Rodas")
    println(mensajeRespuesta)
    
    SimuladorInventarioSistema.validarPatronesYOperadores()
}

// Llamada final al método de ejecución
ejecutarSimulacionCompleta()