#include <stdio.h>  /*file*/
#include <stdlib.h> /*dynamic allocation*/
#include <string.h> /*string*/
#include <ctype.h>  /*string assertion*/
#include "db.h"     /*database API*/

int tokenize_with_id(char *intext, int text_id)
{
    int count = 0;

    /*get first token*/
    char *token = strtok(intext, " ,.\n");

    /*continue getting tokens*/
    while (token != NULL && count < 3000)
    {
        /*save token to database*/
        int result = db_insert_token(text_id, token, count+1);
        if (result < 0) {
            fprintf(stderr, "Failed to save token to database\n");
            return -1;
        }
        
        count++;
        /*get next token*/
        token = strtok(NULL, " ,.\n");
    }

    printf("\nFound and saved %d tokens\n", count);
    return count;
}