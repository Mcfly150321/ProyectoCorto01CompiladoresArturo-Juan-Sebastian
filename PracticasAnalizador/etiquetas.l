%{
#include <stdio.h>
#include <string.h>

int c = 0;

void buscar_etiqueta(const char *linea) {
    const char *ptr = linea;

    while ((ptr = strchr(ptr, '<')) != NULL) {
        
        if (ptr[1] != '\0' && ptr[1] != ' ' && ptr[1] != '/') {
            char nombre[50];
            int i = 0;
            ptr++; 
            
            while (ptr[i] != '\0' && ptr[i] != ' ' && ptr[i] != '>' && i < 49) {
                nombre[i] = ptr[i];
                i++;
            }
            nombre[i] = '\0';
            
            printf(" Etiqueta encontrada: <%s>\n", nombre);
        } else {
            ptr++;
        }
    }
}
%}

%%

[^\n]* { 
    if (yytext[0] != '\0') {
        printf("Linea %d, Texto: %s", c + 1, yytext); 
        printf(", ");
        buscar_etiqueta(yytext);
    }
}

\n { 
    c++; 
}

%%

int main() {
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}