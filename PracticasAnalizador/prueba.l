%{
#include <stdio.h>
#include <string.h>

int c = 1;
%}

%%

"<"[a-zA-Z][a-zA-Z0-9]*(">"|[ \t][^>\n]*">") {

char etiqueta[100];
int i = 0;

while (yytext[i] != ' ' && yytext[i] != '\t' && yytext[i] != '\0') {
    etiqueta[i] = yytext[i];
    i++;
}
etiqueta[i] = '\0';
printf("Encontramos etiqueta %s> en la linea %d\n", etiqueta, c);
}



\n {
    c++;
}

. {
    /* ignorar cualquier otro caracter */
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