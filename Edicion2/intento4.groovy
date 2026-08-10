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
