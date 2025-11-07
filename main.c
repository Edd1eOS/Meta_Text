#include "analyzer.h"  /*tokenizer API*/
#include "db.h"        /*database API*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DB_PATH "analysis.db"
#define MAX_TEXT_LEN 200000

int main() {
    char buf[MAX_TEXT_LEN];
    printf("Please enter text to analyze: ");
    
    // Fix fgets call
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        fprintf(stderr, "Failed to read input\n");
        return 1;
    }
    
    // Remove possible newline character
    size_t len = strlen(buf);
    if (len > 0 && buf[len-1] == '\n') {
        buf[len-1] = '\0';
    }
    
    // Initialize database
    if (db_init(DB_PATH) != 0) {
        fprintf(stderr, "Database initialization failed\n");
        return 1;
    }

    // Insert text into database
    int text_id = db_insert_text(buf);
    if (text_id < 0) {
        fprintf(stderr, "Failed to insert text\n");
        db_close();
        return 1;
    }

    // Perform tokenization
    int result = tokenize_with_id(buf, text_id);
    if (result < 0) {
        fprintf(stderr, "Tokenization process error\n");
        db_close();
        return 1;
    }

    printf("Analysis complete! Text ID: %d\n", text_id);
    db_close();
    return 0;
}