# ProyectoCorto01CompiladoresArturo-Juan-Sebastian

## Rama avances Sebastian

En esta rama estare enviando todos mis avances y este archivo servira para documentar mi Rama.

## Diccionarios propuestos
```

{
"language": "Groovy",
"version": "Apache Groovy 4.x",
"description": "Comprehensive lexical analyzer dictionaries for building a Flex/C lexer or general parser integration.",
"keywords": {
"java_common": [
"abstract", "assert", "boolean", "break", "byte", "case", "catch",
"char", "class", "const", "continue", "default", "do", "double",
"else", "enum", "extends", "false", "final", "finally", "float",
"for", "goto", "if", "implements", "import", "instanceof", "int",
"interface", "long", "native", "new", "null", "package", "private",
"protected", "public", "return", "short", "static", "strictfp",
"super", "switch", "synchronized", "this", "throw", "throws",
"transient", "try", "void", "volatile", "while"
],
"groovy_specific": [
"as", "def", "in", "trait", "property","it","var"
]
},
"operators": [
{ "symbol": "<<=", "token": "OP_ASIG_SL", "description": "Left shift assignment" },
{ "symbol": ">>=", "token": "OP_ASIG_SR", "description": "Right shift assignment" },
{ "symbol": ">>>=", "token": "OP_ASIG_USR", "description": "Unsigned right shift assignment" },
{ "symbol": "=", "token": "OP_ASIG_POW", "description": "Power assignment" },
{ "symbol": "?.", "token": "OP_SAFE_NAV", "description": "Safe navigation operator" },
{ "symbol": ".", "token": "OP_SPREAD_DOT", "description": "Spread operator" },
{ "symbol": "?", "token": "OP_SPREAD_SAFE", "description": "Spread safe operator" },
{ "symbol": "?:", "token": "OP_ELVIS", "description": "Elvis operator" },
{ "symbol": "..", "token": "OP_RANGE_INC", "description": "Inclusive range operator" },
{ "symbol": "..<", "token": "OP_RANGE_EXC", "description": "Exclusive range operator" },
{ "symbol": "=~", "token": "OP_REGEX_FIND", "description": "Regex find operator" },
{ "symbol": "==~", "token": "OP_REGEX_MATCH", "description": "Regex match operator" },
{ "symbol": ".&", "token": "OP_METHOD_PTR", "description": "Method pointer operator" },
{ "symbol": "++", "token": "OP_INC", "description": "Increment" },
{ "symbol": "--", "token": "OP_DEC", "description": "Decrement" },
{ "symbol": "**", "token": "OP_POW", "description": "Power operator" },
{ "symbol": "+=", "token": "OP_ASIG_ADD", "description": "Addition assignment" },
{ "symbol": "-=", "token": "OP_ASIG_SUB", "description": "Subtraction assignment" },
{ "symbol": "=", "token": "OP_ASIG_MUL", "description": "Multiplication assignment" },
{ "symbol": "/=", "token": "OP_ASIG_DIV", "description": "Division assignment" },
{ "symbol": "%=", "token": "OP_ASIG_MOD", "description": "Modulo assignment" },
{ "symbol": "<<", "token": "OP_SL", "description": "Left shift" },
{ "symbol": ">>", "token": "OP_SR", "description": "Right shift" },
{ "symbol": ">>>", "token": "OP_USR", "description": "Unsigned right shift" },
{ "symbol": "==", "token": "OP_EQ", "description": "Equals" },
{ "symbol": "!=", "token": "OP_NEQ", "description": "Not equals" },
{ "symbol": "<=", "token": "OP_LE", "description": "Less than or equal" },
{ "symbol": ">=", "token": "OP_GE", "description": "Greater than or equal" },
{ "symbol": "<=>", "token": "OP_SPACESHIP", "description": "Spaceship comparison operator" },
{ "symbol": "&&", "token": "OP_AND", "description": "Logical AND" },
{ "symbol": "||", "token": "OP_OR", "description": "Logical OR" },
{ "symbol": "+", "token": "PLUS", "description": "Addition" },
{ "symbol": "-", "token": "MINUS", "description": "Subtraction" },
{ "symbol": "*", "token": "MUL", "description": "Multiplication" },
{ "symbol": "/", "token": "DIV", "description": "Division" },
{ "symbol": "%", "token": "MOD", "description": "Modulo" },
{ "symbol": "<", "token": "LT", "description": "Less than" },
{ "symbol": ">", "token": "GT", "description": "Greater than" },
{ "symbol": "=", "token": "ASSIGN", "description": "Assignment" },
{ "symbol": "!", "token": "NOT", "description": "Logical NOT" },
{ "symbol": "&", "token": "BIT_AND", "description": "Bitwise AND" },
{ "symbol": "|", "token": "BIT_OR", "description": "Bitwise OR" },
{ "symbol": "^", "token": "BIT_XOR", "description": "Bitwise XOR" },
{ "symbol": "~", "token": "BIT_NOT", "description": "Bitwise NOT" },
{ "symbol": "?", "token": "QUESTION", "description": "Ternary operator part" },
{ "symbol": ":", "token": "COLON", "description": "Ternary operator part / Map separator" },
{ "symbol": ".", "token": "DOT", "description": "Member access" },
{ "symbol": ",", "token": "COMMA", "description": "Separator" },
{ "symbol": ";", "token": "SEMI", "description": "Statement terminator" }
],
"delimiters": [
{ "symbol": "(", "token": "LPAREN", "description": "Left parenthesis" },
{ "symbol": ")", "token": "RPAREN", "description": "Right parenthesis" },
{ "symbol": "{", "token": "LBRACE", "description": "Left brace" },
{ "symbol": "}", "token": "RBRACE", "description": "Right brace" },
{ "symbol": "[", "token": "LBRACKET", "description": "Left bracket" },
{ "symbol": "]", "token": "RBRACKET", "description": "Right bracket" }
],
"patterns": {
"identifier": "[a-zA-Z_$][a-zA-Z0-9_$]",
"integer": "\d+([lLgG])?",
"float": "\d+\.\d+([eE][+-]?\d+)?([fFdD][gG]?)?",
"single_quote_string": "'([^'\\]|\\.)'",
"double_quote_string": ""([^"\\]|\\.)"",
"triple_quote_string": "("""[^"]""")|('''[^']*''')"
}
}

```
---
# Avances realizados
## Primer reporte completado
### Variables y Contadores del Reporte
Se incorporaron variables de control en C para generar un reporte estadístico completo del archivo fuente analizado:
```
int contador_lineas = 1;
int contador_caracteres = 0; // Conteo exacto mediante yyleng
int contador_enteros = 0;
int contador_float = 0;
int contador_booleanos = 0;
int contador_operadores = 0;
int contador_ids = 0;
```

### Definición de Expresiones Regulares Principales
```
DIGITO   [0-9]
ENTERO   {DIGITO}+
FLOAT    {DIGITO}+\.{DIGITO}+
LETRA    [A-Za-z_$]
ID       {LETRA}({LETRA}|{DIGITO})*
WS       [ \t\r]+
```
* DIGITO / ENTERO: Captura números enteros de una o más cifras.
* FLOAT: Reconoce números de punto flotante con decimales.
* LETRA / ID: Identificadores válidos que inician con letra, guion bajo o símbolo $ permitiendo dígitos subsecuentes.
* WS: Ignora espacios en blanco y tabulaciones horizontales.

Al finalizar el análisis del código fuente, el programa despliega en consola:

1. Cantidad total de líneas de código.

2. Cantidad total de caracteres encontrados (utilizando la longitud del buffer yyleng).
3. Conteo de números enteros.
4. Conteo de números flotantes.
5. Conteo de identificadores.
6. Conteo de valores booleanos (true, false, boolean).
7. Conteo total de operadores aritméticos, lógicos, de asignación y compuestos.
8. Conteo detallado de cada palabra reservada encontrada, ordenado de forma descendente (empleando una estructura de registros en C y ordenamiento qsort).

### Instruciones de ejecucio
```
# 1. Generar el archivo C con Flex
flex proyecto_corto.l

# 2. Compilar con GCC y la librería fl
gcc lex.yy.c -o proyecto_corto -lfl

# 3. Ejecutar pasando un archivo de código fuente de prueba en Groovy
./proyecto_corto < prueba_groovy.txt
```