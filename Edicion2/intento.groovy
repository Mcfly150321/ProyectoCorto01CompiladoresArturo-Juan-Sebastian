// Procesamiento de nomina y calculo de bono
def calcularSalario = 2500.50
int diasTrabajados = 30
boolean esEmpleadoActivo = true
boolean tieneBono = false

if (diasTrabajados >= 15 && esEmpleadoActivo) {
    double totalPagar = calcularSalario + 150.0
    totalPagar *= 1.12
    return totalPagar
} else {
    return 0
}