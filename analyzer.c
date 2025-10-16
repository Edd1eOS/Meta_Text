#include <stdio.h>  /*file*/
#include <stdlib.h> /*dynamic allocation*/
#include <string.h> /*string*/
#include <ctype.h>  /*string assertion*/

int tokenize(char *intext)
{
/*initialize an array to put tokens*/
    char tokens[3000][64];
    int count = 0;

    /*get first token*/
    char *token = strtok(intext, " ,.\n");

    /*continue getting tokens*/
    while (token != NULL && count < 3000)
    {
        /*copy token to array*/
        strncpy(tokens[count], token, 63);
        tokens[count][63] = '\0'; /* ensure null termination */
        count++;

        /*get next token*/
        token = strtok(NULL, " ,.\n");
    }

    /*print tokens for verification*/
    printf("\nFound %d tokens:\n", count);
    for (int i = 0; i < count; i++)
    {
        printf("%d: %s\n", i + 1, tokens[i]);
    }
    return count;
}
int main()
{
    /*get input*/
    char intext[256];
    printf("Enter text: ");
    fgets(intext, sizeof(intext), stdin);

    tokenize(intext);


    return 0;
}