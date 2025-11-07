#include "db.h"
#include <stdio.h>

static sqlite3 *db = NULL; /*The global handle, no need to define later*/
int db_init(const char *db_path) {
    int rc = sqlite3_open(db_path, &db);

    const char *sql = 
        "CREATE TABLE IF NOT EXISTS texts ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "content TEXT NOT NULL"
        ");"
        
        "CREATE TABLE IF NOT EXISTS tokens ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "text_id INTEGER NOT NULL,"
            "token TEXT NOT NULL,"
            "position INTEGER,"
            "FOREIGN KEY(text_id) REFERENCES texts(id)"
        ");"
        
        "CREATE TABLE IF NOT EXISTS stats ("
            "text_id INTEGER PRIMARY KEY,"
            "token_count INTEGER,"
            "avg_len INTEGER,"
            "max_len INTEGER,"
            "min_len INTEGER,"
            "FOREIGN KEY(text_id) REFERENCES texts(id)"
        ");";
    char *err_msg = NULL;
    rc = sqlite3_exec(db, sql, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", err_msg);
        sqlite3_free(err_msg);
        return -1;
}

    
    return 0;
}/*initialize the database*/

int db_insert_text(const char *text){
    const char *sql = "INSERT INTO texts (content) VALUES (?);";
    sqlite3_stmt *stmt;
    int rc;

    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL); /*compile the SQL statement*/
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        return -1;
    }

    sqlite3_bind_text(stmt, 1, text, -1, SQLITE_STATIC); /*bind the text parameter*/
    rc = sqlite3_step(stmt); /*execute the statement*/
    if (rc != SQLITE_DONE) {
        fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        return -1;
    }
    sqlite3_finalize(stmt);
    return (int)sqlite3_last_insert_rowid(db);
};/*insert a new text into the database*/

int db_insert_token(int text_id, const char *token, int position){
    const char *sql = "INSERT INTO tokens (text_id, token, position) VALUES (?, ?, ?);";
    sqlite3_stmt *stmt;
    int rc;

    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL); /*compile the SQL statement*/
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        return -1;
    } /*error handling*/

    sqlite3_bind_int(stmt, 1, text_id);
    sqlite3_bind_text(stmt, 2, token, -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 3, position); /*binding order: text_id, token, position, aligning with the SQL statement*/
    rc = sqlite3_step(stmt); /*execute the statement*/
    if (rc != SQLITE_DONE) {
        fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        return -1;
    }
    

    sqlite3_finalize(stmt);
    return (int)sqlite3_last_insert_rowid(db);
};/*insert a divided token, for later statistical analysis*/

int db_insert_stats(int text_id, int token_count, int avg_len, int max_len, int min_len){
    const char *sql = "INSERT INTO stats (text_id, token_count, avg_len, max_len, min_len) VALUES (?, ?, ?, ?, ?);";
    sqlite3_stmt *stmt; /*define a handle for the prepared statement*/
    int rc;
    rc = sqlite3_prepare_v2(db, sql, -1, &stmt, NULL);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "Failed to prepare statement: %s\n", sqlite3_errmsg(db));
        return -1;
    }

    sqlite3_bind_int(stmt, 1, text_id);
    sqlite3_bind_int(stmt, 2, token_count);
    sqlite3_bind_int(stmt, 3, avg_len);
    sqlite3_bind_int(stmt, 4, max_len);
    sqlite3_bind_int(stmt, 5, min_len); /*binding order: text_id, token_count, avg_len, max_len, min_len*/

    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        fprintf(stderr, "Failed to execute statement: %s\n", sqlite3_errmsg(db));
        sqlite3_finalize(stmt);
        return -1;
    }

    sqlite3_finalize(stmt);
    return 0;


};/*insert statistical data for a text*/

void db_close(void){
    if (db != NULL) {
        int rc = sqlite3_close(db);
        if (rc != SQLITE_OK) {
            fprintf(stderr, "Failed to close database: %s\n", sqlite3_errmsg(db));
        }
        db = NULL; 
    }
};/*close the database connection*/