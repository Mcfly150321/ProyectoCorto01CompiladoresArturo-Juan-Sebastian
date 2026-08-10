%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
//debemos dividir en palabras reservadas, enteros, flotantes, identificadores, booleanos, operadores

int nivel_llaves = 0; // 0 significa ámbito global

typedef enum {
    PR_NINGUNA = 0,
    PR_ABSTRACT, PR_ASSERT, PR_BOOLEAN, PR_BREAK, PR_BYTE,
    PR_CASE, PR_CATCH, PR_CHAR, PR_CLASS, PR_CONST,
    PR_CONTINUE, PR_DEFAULT, PR_DO, PR_DOUBLE, PR_ELSE,
    PR_ENUM, PR_EXTENDS, PR_FALSE, PR_FINAL, PR_FINALLY,
    PR_FLOAT, PR_FOR, PR_GOTO, PR_IF, PR_IMPLEMENTS,
    PR_IMPORT, PR_INSTANCEOF, PR_INT, PR_INTERFACE, PR_LONG,
    PR_NATIVE, PR_NEW, PR_NULL, PR_PACKAGE, PR_PRIVATE,
    PR_PROTECTED, PR_PUBLIC, PR_RETURN, PR_SHORT, PR_STATIC,
    PR_STRICTFP, PR_SUPER, PR_SWITCH, PR_SYNCHRONIZED, PR_THIS,
    PR_THROW, PR_THROWS, PR_TRANSIENT, PR_TRY, PR_TRUE,
    PR_VOID, PR_VOLATILE, PR_WHILE, PR_AS, PR_DEF,
    PR_IN, PR_TRAIT, PR_PROPERTY, PR_IT, PR_VAR,
    TOTAL_PALABRAS_RESERVADAS
} SubtipoReservada;

typedef enum {
    TOKEN_ENTERO,
    TOKEN_FLOTANTE,
    TOKEN_IDENTIFICADOR,
    TOKEN_BOOLEANO,
    TOKEN_OPERADOR,
    TOKEN_RESERVADA
} TipoToken;

const char *nombres_tipos_token[] = {
    "TOKEN_ENTERO",
    "TOKEN_FLOTANTE",
    "TOKEN_IDENTIFICADOR",
    "TOKEN_BOOLEANO",
    "TOKEN_OPERADOR",
    "TOKEN_RESERVADA"
};

typedef struct {
    char lexema[64];  // texto encontrado, por ejemplo: "true", "x", "10.5"
    TipoToken tipo;   // qué tipo de token es
    SubtipoReservada subtipo_pr; // qué palabra reservada es, si aplica
    char ambito[20]; // ámbito en el que se encuentra (global, clase, método, etc.)
    int linea;        // en qué linea del codigo aparecio
} Token;

// Arreglo para llevar la cuenta de cada palabra reservada
int conteo_pr[TOTAL_PALABRAS_RESERVADAS] = {0};

// Nombres de las palabras reservadas en el mismo orden que el enum (sin contar PR_NINGUNA)
const char *nombres_pr[] = {
    "", // Posición 0 coincide con PR_NINGUNA
    "abstract", "assert", "boolean", "break", "byte",
    "case", "catch", "char", "class", "const",
    "continue", "default", "do", "double", "else",
    "enum", "extends", "false", "final", "finally",
    "float", "for", "goto", "if", "implements",
    "import", "instanceof", "int", "interface", "long",
    "native", "new", "null", "package", "private",
    "protected", "public", "return", "short", "static",
    "strictfp", "super", "switch", "synchronized", "this",
    "throw", "throws", "transient", "try", "true",
    "void", "volatile", "while", "as", "def",
    "in", "trait", "property", "it", "var"
};

// Contadores propios
int c_int = 0;
int c_float = 0;
int c_ids = 0;
int c_bool = 0;
int c_ope = 0;
int c_res = 0;
int c_comentarios = 0;
int c_tok = 0;

Token RegTok[2000];

// Definicion de Tokens
#define ID 1

// Palabras Reservadas (indices para el arreglo de conteo)
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

// Variables globales para el reporte
int contador_lineas = 1;
int contador_caracteres = 0;
int contador_enteros = 0;
int contador_float = 0;
int contador_booleanos = 0;
int contador_operadores = 0;
int contador_ids = 0;

void registrar_token(TipoToken tipo) {
    strcpy(RegTok[c_tok].lexema, yytext);
    RegTok[c_tok].tipo = tipo;
    RegTok[c_tok].linea = contador_lineas;
    if (tipo == TOKEN_IDENTIFICADOR)
    {
        if (nivel_llaves == 0) {
            strcpy(RegTok[c_tok].ambito, "global");
        } else {
            strcpy(RegTok[c_tok].ambito, "local");
        }\
    }
     c_tok++;
}

void registrar_palabra_reservada(SubtipoReservada subtipo) {
    strcpy(RegTok[c_tok].lexema, yytext);
    RegTok[c_tok].tipo = TOKEN_RESERVADA;
    RegTok[c_tok].subtipo_pr = subtipo;
    RegTok[c_tok].linea = contador_lineas;
    c_tok++;
    c_res++;
    // Suma 1 a la cuenta individual de esta palabra
    conteo_pr[subtipo]++;
}

// Estructura para ordenar palabras reservadas por frecuencia
typedef struct {
    char palabra[50];
    int conteo;
} InfoPalabra;

// Funcion de comparacion para qsort (orden descendente)
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

"abstract"      { registrar_palabra_reservada(PR_ABSTRACT); }
"assert"        { registrar_palabra_reservada(PR_ASSERT); }
"boolean"       { registrar_palabra_reservada(PR_BOOLEAN); }
"break"         { registrar_palabra_reservada(PR_BREAK); }
"byte"          { registrar_palabra_reservada(PR_BYTE); }
"case"          { registrar_palabra_reservada(PR_CASE); }
"catch"         { registrar_palabra_reservada(PR_CATCH); }
"char"          { registrar_palabra_reservada(PR_CHAR); }
"class"         { registrar_palabra_reservada(PR_CLASS); }
"const"         { registrar_palabra_reservada(PR_CONST); }
"continue"      { registrar_palabra_reservada(PR_CONTINUE); }
"default"       { registrar_palabra_reservada(PR_DEFAULT); }
"do"            { registrar_palabra_reservada(PR_DO); }
"double"        { registrar_palabra_reservada(PR_DOUBLE); }
"else"          { registrar_palabra_reservada(PR_ELSE); }
"enum"          { registrar_palabra_reservada(PR_ENUM); }
"extends"       { registrar_palabra_reservada(PR_EXTENDS); }
"final"         { registrar_palabra_reservada(PR_FINAL); }
"finally"       { registrar_palabra_reservada(PR_FINALLY); }
"float"         { registrar_palabra_reservada(PR_FLOAT); }
"for"           { registrar_palabra_reservada(PR_FOR); }
"goto"          { registrar_palabra_reservada(PR_GOTO); }
"if"            { registrar_palabra_reservada(PR_IF); }
"implements"    { registrar_palabra_reservada(PR_IMPLEMENTS); }
"import"        { registrar_palabra_reservada(PR_IMPORT); }
"instanceof"    { registrar_palabra_reservada(PR_INSTANCEOF); }
"int"           { registrar_palabra_reservada(PR_INT); }
"interface"     { registrar_palabra_reservada(PR_INTERFACE); }
"long"          { registrar_palabra_reservada(PR_LONG); }
"native"        { registrar_palabra_reservada(PR_NATIVE); }
"new"           { registrar_palabra_reservada(PR_NEW); }
"null"          { registrar_palabra_reservada(PR_NULL); }
"package"       { registrar_palabra_reservada(PR_PACKAGE); }
"private"       { registrar_palabra_reservada(PR_PRIVATE); }
"protected"     { registrar_palabra_reservada(PR_PROTECTED); }
"public"        { registrar_palabra_reservada(PR_PUBLIC); }
"return"        { registrar_palabra_reservada(PR_RETURN); }
"short"         { registrar_palabra_reservada(PR_SHORT); }
"static"        { registrar_palabra_reservada(PR_STATIC); }
"strictfp"      { registrar_palabra_reservada(PR_STRICTFP); }
"super"         { registrar_palabra_reservada(PR_SUPER); }
"switch"        { registrar_palabra_reservada(PR_SWITCH); }
"synchronized"  { registrar_palabra_reservada(PR_SYNCHRONIZED); }
"this"          { registrar_palabra_reservada(PR_THIS); }
"throw"         { registrar_palabra_reservada(PR_THROW); }
"throws"        { registrar_palabra_reservada(PR_THROWS); }
"transient"     { registrar_palabra_reservada(PR_TRANSIENT); }
"try"           { registrar_palabra_reservada(PR_TRY); }
"void"          { registrar_palabra_reservada(PR_VOID); }
"volatile"      { registrar_palabra_reservada(PR_VOLATILE); }
"while"         { registrar_palabra_reservada(PR_WHILE); }
"as"            { registrar_palabra_reservada(PR_AS); }
"def"           { registrar_palabra_reservada(PR_DEF); }
"in"            { registrar_palabra_reservada(PR_IN); }
"trait"         { registrar_palabra_reservada(PR_TRAIT); }
"property"      { registrar_palabra_reservada(PR_PROPERTY); }
"it"            { registrar_palabra_reservada(PR_IT); }
"var"           { registrar_palabra_reservada(PR_VAR); }



"true"|"false" {
    contador_caracteres += yyleng;
    registrar_token(TOKEN_BOOLEANO);
    c_bool++;
}
"//".* {
  // los comentarios no se cuentan como operadores
}

"<<="|">>="|"**="|"?."|"?:"|".."|"..<"|"=~"|"==~"|"::"|"++"|"--"|"**"|"+="|"-="|"*="|"/="|"%="|"<<"|">>"|">>>"|"=="|"!="|"<="|">="|"<=>"|"&&"|"||"|"="|"+"|"-"|"*"|"/"|"%"|"!"|"<"|">"|"&"|"|"|"^"|"~"|"?" {
    contador_operadores++;
    contador_caracteres += yyleng;
    registrar_token(TOKEN_OPERADOR);
    c_ope++;
}

[.,:;()\[\]] {
    contador_caracteres += yyleng;
}

"{" {
        contador_caracteres += yyleng;
        nivel_llaves++;
    }

"}" {
        contador_caracteres += yyleng;
        nivel_llaves--;
    }
    

{ID}            { 
    contador_ids++; 
    contador_caracteres += yyleng;
    registrar_token(TOKEN_IDENTIFICADOR);
    c_ids++;
}

{ENTERO}        { 
    contador_enteros++; 
    contador_caracteres += yyleng;

    registrar_token(TOKEN_ENTERO);
    c_int++;
}

{FLOAT}         { 
    contador_float++; 
    contador_caracteres += yyleng;

    registrar_token(TOKEN_FLOTANTE);
    c_float++;
}

.               { 
    contador_caracteres += yyleng; 
}

%%

int yywrap() { return 1; }

int main() {
    yylex();
printf("--- Conteo de Enteros ---\n");
    for (int i = 0; i < c_tok; i++) {
        if (RegTok[i].tipo == TOKEN_ENTERO) {
            printf("Lexema: %s | Linea: %d | Token: %s\n", RegTok[i].lexema, RegTok[i].linea, nombres_tipos_token[RegTok[i].tipo]);
        }
    }

    printf("\n--- Conteo de Flotantes ---\n");
    for (int i = 0; i < c_tok; i++) {
        if (RegTok[i].tipo == TOKEN_FLOTANTE) {
            printf("Lexema: %s | Linea: %d | Token: %s\n", RegTok[i].lexema, RegTok[i].linea, nombres_tipos_token[RegTok[i].tipo]);
        }
    }

    printf("\n--- Conteo de Identificadores ---\n");
    for (int i = 0; i < c_tok; i++) {
        if (RegTok[i].tipo == TOKEN_IDENTIFICADOR) {
            printf("Lexema: %s | Linea: %d | Token: %s | Ambito: %s\n", RegTok[i].lexema, RegTok[i].linea, nombres_tipos_token[RegTok[i].tipo], RegTok[i].ambito);
        }
    }

    printf("\n--- Conteo de Booleanos ---\n");
    for (int i = 0; i < c_tok; i++) {
        if (RegTok[i].tipo == TOKEN_BOOLEANO) {
            printf("Lexema: %s | Linea: %d | Token: %s\n", RegTok[i].lexema, RegTok[i].linea, nombres_tipos_token[RegTok[i].tipo]);
        }
    }

    printf("\n--- Conteo de Operadores ---\n");
    for (int i = 0; i < c_tok; i++) {
        if (RegTok[i].tipo == TOKEN_OPERADOR) {
            printf("Lexema: %s | Linea: %d | Token: %s\n", RegTok[i].lexema, RegTok[i].linea, nombres_tipos_token[RegTok[i].tipo]);
        }
    }

    // --- Filtrar, ordenar e imprimir palabras reservadas ---
    InfoPalabra lista_pr[TOTAL_PALABRAS_RESERVADAS];
    int total_unicas = 0;

    for (int i = 1; i < TOTAL_PALABRAS_RESERVADAS; i++) {
        if (conteo_pr[i] > 0) {
            strcpy(lista_pr[total_unicas].palabra, nombres_pr[i - 1]);
            lista_pr[total_unicas].conteo = conteo_pr[i];
            total_unicas++;
        }
    }

    qsort(lista_pr, total_unicas, sizeof(InfoPalabra), comparar_descendente);

    printf("\n--- Conteo de Palabras Reservadas (Orden Descendente) ---\n");
    for (int i = 0; i < total_unicas; i++) {
        printf("Palabra: %-12s | Apariciones: %d\n", lista_pr[i].palabra, lista_pr[i].conteo);
    }

    printf("\n--- Cantidades Totales ---\n");
    printf("Cantidad de lineas de codigo: %d\n", contador_lineas);
    printf("Cantidad de caracteres encontrados: %d\n", contador_caracteres);
    printf("Cantidad de numeros enteros encontrados: %d\n", c_int);
    printf("Cantidad de numeros flotantes encontrados: %d\n", c_float);
    printf("Cantidad de identificadores encontrados: %d\n", c_ids);
    printf("Cantidad de valores booleanos: %d\n", c_bool);
    printf("Cantidad de operadores encontrados: %d\n", c_ope);
    printf("Cantidad de palabras reservadas encontradas: %d\n", c_res);
    printf("Total general de tokens: %d\n", c_tok);
       return 0;
}