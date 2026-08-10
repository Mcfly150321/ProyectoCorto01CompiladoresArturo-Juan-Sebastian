%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Definicion de Tokens
#define ID 1

// Palabras Reservadas (Indices para nuestro arreglo de conteo)
#define PR_ABSTRACT 2
#define PR_ASSERT 3
#define PR_BOOLEAN 4
#define PR_BREAK 5
#define PR_BYTE 6
#define PR_CASE 7
#define PR_CATCH 8
#define PR_CHAR 9
#define PR_CLASS 10
#define PR_CONST 11
#define PR_CONTINUE 12
#define PR_DEFAULT 13
#define PR_DO 14
#define PR_DOUBLE 15
#define PR_ELSE 16
#define PR_ENUM 17
#define PR_EXTENDS 18
#define PR_FALSE 19
#define PR_FINAL 20
#define PR_FINALLY 21
#define PR_FLOAT 22
#define PR_FOR 23
#define PR_GOTO 24
#define PR_IF 25
#define PR_IMPLEMENTS 26
#define PR_IMPORT 27
#define PR_INSTANCEOF 28
#define PR_INT 29
#define PR_INTERFACE 30
#define PR_LONG 31
#define PR_NATIVE 32
#define PR_NEW 33
#define PR_NULL 34
#define PR_PACKAGE 35
#define PR_PRIVATE 36
#define PR_PROTECTED 37
#define PR_PUBLIC 38
#define PR_RETURN 39
#define PR_SHORT 40
#define PR_STATIC 41
#define PR_STRICTFP 42
#define PR_SUPER 43
#define PR_SWITCH 44
#define PR_SYNCHRONIZED 45
#define PR_THIS 46
#define PR_THROW 47
#define PR_THROWS 48
#define PR_TRANSIENT 49
#define PR_TRY 50
#define PR_TRUE 51
#define PR_VOID 52
#define PR_VOLATILE 53
#define PR_WHILE 54
#define PR_AS 55
#define PR_DEF 56
#define PR_IN 57
#define PR_TRAIT 58
#define PR_PROPERTY 59
#define PR_IT 60
#define PR_VAR 61

// Operadores y otros tokens (del 62 en adelante)
#define OP_ASIG_SL 62
// ... (puedes mantener tus defines de operadores igual)

// Estructura para llevar el conteo de palabras reservadas
typedef struct {
    const char *nombre;
    int conteo;
} InfoPalabra;

// Tabla con todas las palabras reservadas que buscas
InfoPalabra tabla_pr[] = {
    {"abstract", 0}, {"assert", 0}, {"boolean", 0}, {"break", 0}, {"byte", 0},
    {"case", 0}, {"catch", 0}, {"char", 0}, {"class", 0}, {"const", 0},
    {"continue", 0}, {"default", 0}, {"do", 0}, {"double", 0}, {"else", 0},
    {"enum", 0}, {"extends", 0}, {"false", 0}, {"final", 0}, {"finally", 0},
    {"float", 0}, {"for", 0}, {"goto", 0}, {"if", 0}, {"implements", 0},
    {"import", 0}, {"instanceof", 0}, {"int", 0}, {"interface", 0}, {"long", 0},
    {"native", 0}, {"new", 0}, {"null", 0}, {"package", 0}, {"private", 0},
    {"protected", 0}, {"public", 0}, {"return", 0}, {"short", 0}, {"static", 0},
    {"strictfp", 0}, {"super", 0}, {"switch", 0}, {"synchronized", 0}, {"this", 0},
    {"throw", 0}, {"throws", 0}, {"transient", 0}, {"try", 0}, {"true", 0},
    {"void", 0}, {"volatile", 0}, {"while", 0}, {"as", 0}, {"def", 0},
    {"in", 0}, {"trait", 0}, {"property", 0}, {"it", 0}, {"var", 0}
};
int total_pr_registradas = 60;

// Variables globales para el reporte
int contador_lineas = 1;
int contador_caracteres = 0;
int contador_enteros = 0;
int contador_float = 0;
int contador_booleanos = 0;
int contador_operadores = 0;
int contador_ids = 0;

// Función auxiliar para sumarizar la palabra reservada encontrada
void registrar_pr(const char *palabra) {
    for (int i = 0; i < total_pr_registradas; i++) {
        if (strcmp(tabla_pr[i].nombre, palabra) == 0) {
            tabla_pr[i].conteo++;
            if (strcmp(palabra, "boolean") == 0 || strcmp(palabra, "true") == 0 || strcmp(palabra, "false") == 0) {
                contador_booleanos++;
            }
            break;
        }
    }
}

// Función de comparación para ordenar de forma descendente (de mayor a menor)
int comparar_descendente(const void *a, const void *b) {
    InfoPalabra *p1 = (InfoPalabra *)a;
    InfoPalabra *p2 = (InfoPalabra *)b;
    return p2->conteo - p1->conteo; 
}
%}

DIGITO   [0-9]
ENTERO   {DIGITO}+
FLOAT    {DIGITO}+\.{DIGITO}+
LETRA    [A-Za-z_$]
ID       {LETRA}({LETRA}|{DIGITO})*
WS       [ \t\r]+

%%

\n              { contador_lineas++; contador_caracteres += yyleng; }
{WS}            { contador_caracteres += yyleng; /* Ignorar espacios pero sumarlos al total de caracteres */ }

"abstract"|"assert"|"boolean"|"break"|"byte"|"case"|"catch"|"char"|"class"|"const"|"continue"|"default"|"do"|"double"|"else"|"enum"|"extends"|"false"|"final"|"finally"|"float"|"for"|"goto"|"if"|"implements"|"import"|"instanceof"|"int"|"interface"|"long"|"native"|"new"|"null"|"package"|"private"|"protected"|"public"|"return"|"short"|"static"|"strictfp"|"super"|"switch"|"synchronized"|"this"|"throw"|"throws"|"transient"|"try"|"true"|"void"|"volatile"|"while"|"as"|"def"|"in"|"trait"|"property"|"it"|"var" {
    registrar_pr(yytext);
    contador_caracteres += yyleng;
    printf("Token: PR_%s\n", yytext);
}

"<<="|"ве="|"|>>="|"**="|"?."|"*."|"?*\""|"?:"|".."|'..<|"=~"|"==~"|"::"|"++"|"--"|"**"|"+="|"-="|"*="|"/="|"%="|"<<"|">>"|">>>"|"=="|"!="|"<="|">="|"<=>"|"&&"|"||"|"="|"+"|"-"|"*"|"/"|"%"|"!"|"<"|">"|"&"|"|"|"^"|"~"|"\?" {
    contador_operadores++;
    contador_caracteres += yyleng;
    printf("Token: OPERADOR -> Lexema: %s\n", yytext);
}


[.,:;(){}\[\]] {
    contador_caracteres += yyleng;
    printf("Token: DELIMITADOR/PUNTUACION -> Lexema: %s\n", yytext);
}

{ID}            { 
    contador_ids++; 
    contador_caracteres += yyleng;
    printf("Token: ID -> Lexema: %s\n", yytext); 
}

{ENTERO}        { 
    contador_enteros++; 
    contador_caracteres += yyleng;
    printf("Token: ENTERO -> Lexema: %s\n", yytext); 
}

{FLOAT}         { 
    contador_float++; 
    contador_caracteres += yyleng;
    printf("Token: FLOAT -> Lexema: %s\n", yytext); 
}

.               { 
    contador_caracteres += yyleng; 
}

%%

int yywrap() { return 1; }

int main() {
    yylex();

    // Ordenar las palabras reservadas de mayor a menor frecuencia
    qsort(tabla_pr, total_pr_registradas, sizeof(InfoPalabra), comparar_descendente);

    printf("\n========================================");
    printf("\n               REPORTE 1                ");
    printf("\n========================================");
    printf("\n- Cantidad de lineas de codigo: %i", contador_lineas);
    printf("\n- Cantidad de caracteres encontrados: %i", contador_caracteres);
    printf("\n- Cantidad de numeros enteros encontrados: %i", contador_enteros);
    printf("\n- Cantidad de numeros flotantes encontrados: %i", contador_float);
    printf("\n- Cantidad de identificadores encontrados: %i", contador_ids);
    printf("\n- Cantidad de valores booleanos: %i", contador_booleanos);
    printf("\n- Cantidad de operadores encontrados: %i", contador_operadores);
    
    printf("\n\n--- Conteo de Palabras Reservadas (Orden Descendente) ---");
    for (int i = 0; i < total_pr_registradas; i++) {
        if (tabla_pr[i].conteo > 0) {
            printf("\n  > %s: %d", tabla_pr[i].nombre, tabla_pr[i].conteo);
        }
    }
    printf("\n========================================\n");
    return 0;
}