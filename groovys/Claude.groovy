// Jerarquía sellada de figuras geométricas
sealed abstract class Figura permits Circulo, Cuadrado, Triangulo {
    abstract double area()
}

class Circulo extends Figura {
    double radio
    Circulo(double radio) { this.radio = radio }
    double area() { Math.PI * radio ** 2 }
}

class Cuadrado extends Figura {
    double lado
    Cuadrado(double lado) { this.lado = lado }
    double area() { lado * lado }
}

// non-sealed: reabre esta rama para que cualquiera la extienda
non-sealed class Triangulo extends Figura {
    double base, altura
    Triangulo(double base, double altura) {
        this.base = base
        this.altura = altura
    }
    double area() { (base * altura) / 2 }
}

// def y var: dos formas de declarar variables
def figuras = [
    new Circulo(5),
    new Cuadrado(4),
    new Triangulo(6, 3)
]

var total = 0.0

figuras.each { fig ->
    // switch expression con yield
    String tipo = switch (fig) {
        case Circulo   -> "círculo"
        case Cuadrado  -> "cuadrado"
        case Triangulo -> "triángulo"
        default -> {
            yield "figura desconocida"
        }
    }

    def area = fig.area()
    total += area

    println "Es un ${tipo} con área de ${area.round(2)}"
}

println "Área total: ${total.round(2)}"