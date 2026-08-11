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
// --- Extensiones y análisis adicionales de las figuras ---

// 1. Filtrar figuras cuyo área sea mayor a un umbral específico usando findAll
def umbral = 15.0
def figurasGrandes = figuras.findAll { it.area() > umbral }
println "\n--- Análisis de figuras con área mayor a ${umbral} ---"
figurasGrandes.each { f ->
    println "Figura ${f.class.simpleName} supera el umbral con ${f.area().round(2)}"
}

// 2. Uso de collect para transformar la lista de objetos en una lista de mapas con sus propiedades
def resumenFiguras = figuras.collect { f ->
    [tipo: f.class.simpleName, areaRedondeada: f.area().round(2)]
}

// 3. Imprimir el resumen utilizando un formato tabular limpio
println "\n--- Resumen Tabular de Figuras ---"
resumenFiguras.eachWithIndex { item, index ->
    println "${index + 1}. [${item.tipo}] -> Área: ${item.areaRedondeada}"
}

// 4. Encontrar la figura con mayor área utilizando max
def figuraMayor = figuras.max { it.area() }
println "\nLa figura con mayor área es un ${figuraMayor.class.simpleName} con ${figuraMayor.area().round(2)}"