%{
#include <stdio.h>
#include <stdlib.h>

// Definicion de Tokens
// Identificadores
#define ID 1

// Palabras Reservadas
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

// Operadores de asignacion
#define OP_ASIG_SL 62
#define OP_ASIG_SR 63
#define OP_ASIG_USR 64
#define OP_ASIG_POW 65

// Navigation operators
#define OP_SAFE_NAV 66

// Spread Operators
#define OP_SPREAD_DOT 67
#define OP_SPREAD_SAFE 68
#define OP_ELVIS 69
#define OP_RANGE_INC 70
#define OP_RANGE_EXC 71
#define OP_REGEX_FIND 72
#define OP_REGEX_MATCH 73
#define OP_METHOD_PTR 74

// Operadores matematicos
#define OP_INC 75
#define OP_DEC 76
#define OP_POW 77
#define OP_ASIG_ADD 78
#define OP_ASIG_SUB 79
#define OP_ASIG_MUL 80
#define OP_ASIG_DIV 81
#define OP_ASIG_MOD 82

// Operadores 
#define OP_SL 83
#define OP_SR 84
#define OP_USR 85

// Operadores de comparacion
#define OP_EQ 86
#define OP_NEQ 87
#define OP_LE 88
#define OP_GE 89
#define OP_SPACEHCIP 90
#define OP_AND 91
#define OP_OR 92

// Operadores aritmeticos
#define PLUS 93
#define MINUS 94
#define MULT 95
#define DIV 96
#define MOD 97
#define OP_ASSIG 98
#define NOT 99
#define LT 100

// Defincion de variables
int contador_lineas = 0;
int contador_caracteres = 0;
int contador_enteros = 0;
%}

DIGITO   [0-9]
ENTERO   {DIGITO}+
LETRA    [A-Za-z_$]
ID       {LETRA}({LETRA}|{DIGITO})*
WS       [ \t\r]+

%%

\n              { contador_lineas++; }
{WS}            { /* Ignorar espacios y tabulaciones */ }

"abstract"      { printf("Token: PR_ABSTRACT\n"); }
"assert"        { printf("Token: PR_ASSERT\n"); }
"boolean"       { printf("Token: PR_BOOLEAN\n"); }
"break"         { printf("Token: PR_BREAK\n"); }
"byte"          { printf("Token: PR_BYTE\n"); }
"case"          { printf("Token: PR_CASE\n"); }
"catch"         { printf("Token: PR_CATCH\n"); }
"char"          { printf("Token: PR_CHAR\n"); }
"class"         { printf("Token: PR_CLASS\n"); }
"const"         { printf("Token: PR_CONST\n"); }
"continue"      { printf("Token: PR_CONTINUE\n"); }
"default"       { printf("Token: PR_DEFAULT\n"); }
"do"            { printf("Token: PR_DO\n"); }
"double"        { printf("Token: PR_DOUBLE\n"); }
"else"          { printf("Token: PR_ELSE\n"); }
"enum"          { printf("Token: PR_ENUM\n"); }
"extends"       { printf("Token: PR_EXTENDS\n"); }
"false"         { printf("Token: PR_FALSE\n"); }
"final"         { printf("Token: PR_FINAL\n"); }
"finally"       { printf("Token: PR_FINALLY\n"); }
"float"         { printf("Token: PR_FLOAT\n"); }
"for"           { printf("Token: PR_FOR\n"); }
"goto"          { printf("Token: PR_GOTO\n"); }
"if"            { printf("Token: PR_IF\n"); }
"implements"    { printf("Token: PR_IMPLEMENTS\n"); }
"import"        { printf("Token: PR_IMPORT\n"); }
"instanceof"    { printf("Token: PR_INSTANCEOF\n"); }
"int"           { printf("Token: PR_INT\n"); }
"interface"     { printf("Token: PR_INTERFACE\n"); }
"long"          { printf("Token: PR_LONG\n"); }
"native"        { printf("Token: PR_NATIVE\n"); }
"new"           { printf("Token: PR_NEW\n"); }
"null"          { printf("Token: PR_NULL\n"); }
"package"       { printf("Token: PR_PACKAGE\n"); }
"private"       { printf("Token: PR_PRIVATE\n"); }
"protected"     { printf("Token: PR_PROTECTED\n"); }
"public"        { printf("Token: PR_PUBLIC\n"); }
"return"        { printf("Token: PR_RETURN\n"); }
"short"         { printf("Token: PR_SHORT\n"); }
"static"        { printf("Token: PR_STATIC\n"); }
"strictfp"      { printf("Token: PR_STRICTFP\n"); }
"super"         { printf("Token: PR_SUPER\n"); }
"switch"        { printf("Token: PR_SWITCH\n"); }
"synchronized"  { printf("Token: PR_SYNCHRONIZED\n"); }
"this"          { printf("Token: PR_THIS\n"); }
"throw"         { printf("Token: PR_THROW\n"); }
"throws"        { printf("Token: PR_THROWS\n"); }
"transient"     { printf("Token: PR_TRANSIENT\n"); }
"try"           { printf("Token: PR_TRY\n"); }
"true"          { printf("Token: PR_TRUE\n"); }
"void"          { printf("Token: PR_VOID\n"); }
"volatile"      { printf("Token: PR_VOLATILE\n"); }
"while"         { printf("Token: PR_WHILE\n"); }

"as"            { printf("Token: PR_AS\n"); }
"def"           { printf("Token: PR_DEF\n"); }
"in"            { printf("Token: PR_IN\n"); }
"trait"         { printf("Token: PR_TRAIT\n"); }
"property"      { printf("Token: PR_PROPERTY\n"); }
"it"            { printf("Token: PR_IT\n"); }
"var"           { printf("Token: PR_VAR\n"); }

"<<="           { printf("Token: OP_ASIG_SL\n"); }
">>="           { printf("Token: OP_ASIG_SR\n"); }
">>>="          { printf("Token: OP_ASIG_USR\n"); }
"="             { printf("Token: OP_ASIG\n");}
"?."            { printf("Token: OP_SAFE_NAV\n"); }
"."             { printf("Token: OP_SPREAD_DOT\n"); }
"?"             { printf("Token: OP_SPREAD_SAFE\n");}
"?:"            { printf("Token: OP_ELVIS\n");}
".."            { printf("Token: OP_RANGE_INC\n");}
"..<"           { printf("Token: OP_RANGE_EXC\n");}
"=~"            { printf("Token: OP_REGEX_FIND\n");}
"==~"           { printf("Token: OP_REGEX_MATCH\n");}
"::"            { printf("Token: OP_METHOD_PTR\n");}
"++"            { printf("Token: OP_INC\n");}
"--"            { printf("Token: OP_DEC\n"); }
"**"            { printf("Token: OP_POW\n"); }
"+="            { printf("Token: OP_ASIG_ADD\n"); }
"-="            { printf("Token: OP_ASIG_SUB\n"); }
"*="            { printf("Token: OP_ASIG_MUL\n"); }
"/="            { printf("Token: OP_ASIG_DIV\n"); }
"%="            { printf("Token: OP_ASIG_MOD\n"); }
"<<"            { printf("Token: OP_SL\n"); }
">>"            { printf("Token: OP_SR\n"); }
">>>"           { printf("Token: OP_USR\n"); }
"=="            { printf("Token: OP_EQ\n"); }
"!="            { printf("Token: OP_NEQ\n"); }
"<="            { printf("Token: OP_LE\n"); }
">="            { printf("Token: OP_GE\n"); }
"<=>"           { printf("Token: OP_SPACEHCIP\n"); }
"&&"            { printf("Token: OP_AND\n"); }
"||"            { printf("Token: OP_OR\n"); }
"+"             { printf("Token: PLUS\n"); }
"-"             { printf("Token: MINUS\n"); }
"*"             { printf("Token: MULT\n"); }
"/"             { printf("Token: DIV\n"); }
"%"             { printf("Token: MOD\n"); }
"<"             { printf("Token: LT\n"); }


{ID}            { printf("Token: ID -> Lexema: %s\n", yytext); }
{ENTERO}        { contador_enteros++; printf("Token: ENTERO -> Lexema: %s\n", yytext); }

.               { contador_caracteres++; }

%%

int yywrap() { return 1; }

int main() {
    yylex();
    printf("\n--- Resumen ---");
    printf("\nTotal de lineas: %i", contador_lineas);
    printf("\nTotal de caracteres (no reconocidos/sueltos): %i", contador_caracteres);
    printf("\nTotal de enteros: %i\n", contador_enteros);
    return 0;
}