#include <stdio.h> /*file*/
#include <stdlib.h> /*dynamic allocation*/
#include <string.h> /*string*/
#include <ctype.h> /*string assertion*/

#ifndef ANALYZER_H
#define ANALYZER_H
#define MAX_TOKENS 3000
#define MAX_TOKEN_LEN 64

int tokenize_with_id(char *intext, int text_id);

#endif