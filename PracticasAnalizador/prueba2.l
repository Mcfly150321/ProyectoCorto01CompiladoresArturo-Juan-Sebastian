%{
#include <stdio.h>
#include <string.h>
typedef struct {
    char etiqueta[50];
    int linea;
} etiqueta;


typedef struct {
    char id[50];
    int linea;
} ids;

typedef struct {
    char clase[50];
    int linea;
} class;

typedef struct {
    char nombre[50];
    int linea;
} archivo;

int  contadorcaracteres=0;


etiqueta Et[100];
int contadoretiquetas=0;
int c = 1;



ids Id[100];
int contadorid=0;

class Clase[100];
int contadorclase=0;

archivo Arch[100];
int contadorarch=0;


void extraer_valor(char *texto, char *destino) {
    int i = 0;
    int j = 0;

    while (texto[i] != '"' && texto[i] != '\0') {
        i++;
    }

    if (texto[i] == '"') {
        i++;
    }

    while (texto[i] != '"' && texto[i] != '\0') {
        destino[j] = texto[i];
        i++;
        j++;
    }

    destino[j] = '\0';
}

%}


%x TAG

%%

"<"[a-zA-Z][a-zA-Z0-9]* {
    contadorcaracteres += yyleng;

    BEGIN(TAG);
    strcpy(Et[contadoretiquetas].etiqueta, yytext);
    strcat(Et[contadoretiquetas].etiqueta, ">");
    Et[contadoretiquetas].linea = c;
    contadoretiquetas++;
}

<TAG>id[ \t]*=[ \t]*\"[^\"]*\" {
    char nombre[100];

    contadorcaracteres += yyleng;

    extraer_valor(yytext, nombre);
    strcpy(Id[contadorid].id, nombre);
    Id[contadorid].linea = c;
    contadorid++;
}

<TAG>class[ \t]*=[ \t]*\"[^\"]*\" {
    char nombre[100];

    contadorcaracteres += yyleng;

    extraer_valor(yytext, nombre);
    strcpy(Clase[contadorclase].clase, nombre);
    Clase[contadorclase].linea = c;
    contadorclase++;
}

<TAG>src[ \t]*=[ \t]*\"[^\"]*\.js\" {
    char nombre[100];

    contadorcaracteres += yyleng;

    extraer_valor(yytext, nombre);
    strcpy(Arch[contadorarch].nombre, nombre);
    Arch[contadorarch].linea = c;
    contadorarch++;
}

<TAG>href[ \t]*=[ \t]*\"[^\"]*\.css\" {
    char nombre[100];

    contadorcaracteres += yyleng;

    extraer_valor(yytext, nombre);
    strcpy(Arch[contadorarch].nombre, nombre);
    Arch[contadorarch].linea = c;
    contadorarch++;
}

<TAG>">" {
    contadorcaracteres += yyleng;

    BEGIN(INITIAL);
}

<TAG>\n {
    contadorcaracteres += yyleng;

    c++;
    BEGIN(INITIAL);
}

\n {
    contadorcaracteres += yyleng;

    c++;
}

<TAG>. {
    contadorcaracteres += yyleng;

}

. {
    contadorcaracteres += yyleng;

}

%%

int main() {
    yylex();
    printf("\n\n--- REPORTE DE ETIQUETAS GUARDADAS ---\n");
    for (int i = 0; i < contadoretiquetas; i++) {
        printf(" Etiqueta: %s | Linea: %d\n", Et[i].etiqueta, Et[i].linea);
    }
    printf("Total: %d", contadoretiquetas);

printf("\n\n--- REPORTE DE IDS GUARDADOS ---\n");
    for (int i = 0; i < contadorid; i++) {
        printf("Id: %s | Linea: %d\n", Id[i].id, Id[i].linea);
    }
    printf("Total: %d", contadorid);


printf("\n\n--- REPORTE DE CLASES GUARDADAS ---\n");
    for (int i = 0; i < contadorclase; i++) {
        printf("Clase: %s | Linea: %d\n", Clase[i].clase, Clase[i].linea);
    }
    printf("Total: %d", contadorclase);

printf("\n\n--- REPORTE DE ARCHIVOS GUARDADOS ---\n");
    for (int i = 0; i < contadorarch; i++) {
        printf("Arthivo: %s | Linea: %d\n", Arch[i].nombre, Arch[i].linea);
    }
    printf("Total: %d", contadorarch);

printf("\n\n--- REPORTE CARACTERES TOTALES ---\n");
    printf(" %d", contadorcaracteres);

    return 0;
}

int yywrap() {
    return 1;
}
