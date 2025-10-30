#ifndef DB_H
#define DB_H

/* The head of "database", contains macrodefs, func prototypes only*/

#include <sqlite3.h>
#include <stdio.h>
#define DB_PATH "data.db"

int db_init(const char *db_path);/*initialize the database*/

int db_insert_text(const char *text);/*insert a new text into the database*/

int db_insert_token(int text_id, const char *token, int position);/*insert a divided token, for later statistical analysis*/

int db_insert_stats(int text_id, int token_count, int avg_len, int max_len, int min_len);/*insert statistical data for a text*/

void db_close(void);/*close the database connection*/
#endif