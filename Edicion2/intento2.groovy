// Variables globales del script
double salarioBase = 3500.00
int bonificacionGlobal = 250
boolean esEmpresaActiva = true

// Definición de función
def calcularNomina(int diasTrabajados, double tarifaDiaria) {
    // Declaraciones locales dentro de la función
    double totalDevengado = diasTrabajados * tarifaDiaria
    double impuestoLocal = 0.05
    
    if (diasTrabajados >= 20 && esEmpresaActiva) {
        totalDevengado += bonificacionGlobal
    }
    
    // Reuso de variable local sin palabra reservada/def
    totalDevengado -= (totalDevengado * impuestoLocal)
    
    return totalDevengado
}

// Uso de la función
double liquidoAPagar = calcularNomina(22, 160.0)
return liquidoAPagar
