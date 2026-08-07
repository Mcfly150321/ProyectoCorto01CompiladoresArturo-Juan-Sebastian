%{
#include <stdio.h>
#include <string.h>

int c = 0;

char* buscar_etiqueta(const char *linea) {
    static char out_etiqueta[50];
    const char *ptr = strchr(linea, '<');
     
     if (ptr != NULL && ptr[1] != '!' && ptr[1] != '\0' && ptr[1] != ' ' && ptr[1] != '/') {
    int i = 0;
    ptr++; 
    
    while (ptr[i] != '\0' && ptr[i] != ' ' && ptr[i-1] != '/' && ptr[i] != '>' && i < 49) {
        out_etiqueta[i] = ptr[i];
        i++;
    }
    out_etiqueta[i] = '\0';
    return out_etiqueta;
}
  
    
    return NULL;
}
%}

%%

[^\n]* { 
    if (yytext[0] != '\0') {
        char *eti = buscar_etiqueta(yytext);

        if (eti != NULL) {
            printf("Linea %d: Se encontró la etiqueta <%s>\n", c + 1, eti);
        } 
    }
}

\n { 
    c++; 
}

%%

int main() {
    printf("Etiquetas encontradas \n");
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}