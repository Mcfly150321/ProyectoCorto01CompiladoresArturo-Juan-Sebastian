%{
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_TAGS 200

/* --- Estructura para el conteo de etiquetas --- */
typedef struct {
    char nombre[64];
    int  cantidad;
} TagCount;

TagCount tags[MAX_TAGS];
int  num_tags = 0;
long total_chars = 0;      /* Total de caracteres del documento */
int  es_cierre = 0;        /* 1 si la etiqueta actual es de cierre </...> */
char etiqueta_actual[64] = "";

/* Busca/crea la etiqueta en la tabla de conteo y suma 1 */
void contar_etiqueta(char *nombre) {
    int i;
    for (i = 0; i < num_tags; i++) {
        if (strcmp(tags[i].nombre, nombre) == 0) {
            tags[i].cantidad++;
            return;
        }
    }
    if (num_tags < MAX_TAGS) {
        strncpy(tags[num_tags].nombre, nombre, sizeof(tags[num_tags].nombre) - 1);
        tags[num_tags].cantidad = 1;
        num_tags++;
    }
}

/* Extrae el valor entre comillas de un texto tipo  id="valor" */
char *valor_atributo(char *texto) {
    static char buffer[256];
    char *inicio = strchr(texto, '"');
    char *fin;
    if (!inicio) { buffer[0] = '\0'; return buffer; }
    inicio++;
    fin = strchr(inicio, '"');
    if (!fin) { buffer[0] = '\0'; return buffer; }
    if (fin - inicio > 255) fin = inicio + 255;
    strncpy(buffer, inicio, fin - inicio);
    buffer[fin - inicio] = '\0';
    return buffer;
}
%}

%option noyywrap
%option yylineno

%x TAGNAME
%x TAG

%%

    /* Comentarios <!-- --> y declaraciones <!DOCTYPE ...>: se consumen y no se imprimen */
"<!"[^>]*">"                         { total_chars += yyleng; }

    /* Apertura de etiqueta de cierre </...>  */
"</"                                  { total_chars += yyleng; es_cierre = 1; BEGIN(TAGNAME); }

    /* Apertura de etiqueta normal <...> */
"<"                                   { total_chars += yyleng; es_cierre = 0; BEGIN(TAGNAME); }

    /* Nombre de la etiqueta (justo después de "<" o "</") */
<TAGNAME>[a-zA-Z][a-zA-Z0-9]*         {
                                          total_chars += yyleng;
                                          strncpy(etiqueta_actual, yytext, sizeof(etiqueta_actual) - 1);
                                          if (!es_cierre) {
                                              printf("<%s>  (linea %d)\n", yytext, yylineno);
                                              contar_etiqueta(yytext);
                                          }
                                          BEGIN(TAG);
                                       }

    /* Atributo id="..." */
<TAG>"id"[ \t]*=[ \t]*\"[^\"]*\"       {
                                          total_chars += yyleng;
                                          printf("id : %s\n", valor_atributo(yytext));
                                       }

    /* Atributo class="..." */
<TAG>"class"[ \t]*=[ \t]*\"[^\"]*\"    {
                                          total_chars += yyleng;
                                          printf("clase : %s\n", valor_atributo(yytext));
                                       }

    /* Atributo href="..." : archivo .css solo si la etiqueta es <link> */
<TAG>"href"[ \t]*=[ \t]*\"[^\"]*\"     {
                                          total_chars += yyleng;
                                          char *val = valor_atributo(yytext);
                                          int len = strlen(val);
                                          if (strcmp(etiqueta_actual, "link") == 0 &&
                                              len > 4 && strcmp(val + len - 4, ".css") == 0) {
                                              printf("archivo: %s\n", val);
                                          }
                                       }

    /* Atributo src="..." : archivo .js solo si la etiqueta es <script> */
<TAG>"src"[ \t]*=[ \t]*\"[^\"]*\"      {
                                          total_chars += yyleng;
                                          char *val = valor_atributo(yytext);
                                          int len = strlen(val);
                                          if (strcmp(etiqueta_actual, "script") == 0 &&
                                              len > 3 && strcmp(val + len - 3, ".js") == 0) {
                                              printf("archivo: %s\n", val);
                                          }
                                       }

    /* Cualquier otro atributo con valor entre comillas: se descarta */
<TAG>\"[^\"]*\"                       { total_chars += yyleng; }

    /* Fin de la etiqueta */
<TAG>">"                              { total_chars += yyleng; BEGIN(INITIAL); }

    /* Cualquier otro caracter dentro de la etiqueta (nombres de atributo, '=', espacios) */
<TAG>\n                               { total_chars += yyleng; }
<TAG>.                                { total_chars += yyleng; }

    /* Texto normal fuera de etiquetas */
\n                                    { total_chars += yyleng; }
.                                     { total_chars += yyleng; }

%%

int main(void) {
    int i;

    yylex();

    printf("\n--- Conteo de etiquetas ---\n");
    for (i = 0; i < num_tags; i++) {
        printf("%s : %d\n", tags[i].nombre, tags[i].cantidad);
    }

    printf("\nTotal de caracteres del documento: %ld\n", total_chars);

    return 0;
}
