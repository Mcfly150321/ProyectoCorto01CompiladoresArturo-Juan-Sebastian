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
