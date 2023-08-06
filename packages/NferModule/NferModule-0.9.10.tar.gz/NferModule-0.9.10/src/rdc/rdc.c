/*
 * rdc.c - Ross Data Compression (RDC)
 *         driver program
 *
 * This program will compress or decompress a file
 * using RDC data compression.  It will also perform some preprocessing
 * needed for reducing the size of code included for the nfer compiler.
 *
 * Parts adapted from TESTRDC.C Written by Ed Ross, 1/92
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <stdint.h>

#include "log.h"
#include "rdc.h"

FILE   *infile, *outfile;       /* FILE access */

char   usage[] =
        "Usage: rdc <c | d | s> <infile> <outfile>\n"
        "       c = compress infile to outfile\n"
        "       d = decompress infile to outfile\n"
        "       s = strip comments and includes\n";

typedef enum {
    BEGINNING_OF_LINE,
    SCANNING,
    POUND,
    POUNDI,
    POUNDIN,
    POUNDINC,
    POUNDINCL,
    POUNDINCLU,
    POUNDINCLUD,
    POUNDINCLUDE,
    SLASH,
    LINE_COMMENT,
    BLOCK_COMMENT,
    STAR
} strip_dfa_states;

static void strip_comments_and_includes(FILE *infile, FILE *outfile) {
    int bytes_read, gap;
    uint8_t *index, *anchor, *out_index, c;
    strip_dfa_states state;

    uint8_t inbuff[RDC_IO_BUFFER_LENGTH];     /* io buffers */
    uint8_t outbuff[RDC_IO_BUFFER_LENGTH];

    /* read infile BUFF_LEN bytes at a time */
    index = inbuff;
    anchor = index;
    gap = 0;
    state = BEGINNING_OF_LINE;

    while ((bytes_read = fread(index, 1, RDC_IO_BUFFER_LENGTH - gap, infile)) > 0) {
        out_index = outbuff;

        /* nothing was read */
        if (bytes_read == 0) {
            /* check for read errors */
            if (ferror(infile)) {
                perror("An error occurred while reading.\n");
                return;
            } else {
                /* otherwise, presumably we reached eof */
                return;
            }
        }

        /* scan through, looking for #include directives */
        while (bytes_read--) {
            c = *index++;

            switch(state) {
            case BEGINNING_OF_LINE:
                if (c == ' ' || c == '\t' || c == '\r' || c == '\n') {
                    state = BEGINNING_OF_LINE;
                } else if (c == '#') {
                    state = POUND;
                } else if (c == '/') {
                    state = SLASH;
                } else {
                    state = SCANNING;
                }
                break;
            case SCANNING:
                if (c == '/') {
                    state = SLASH;
                } else {
                    if (c == '\n') {
                        state = BEGINNING_OF_LINE;
                    }
                    /* copy into the out buffer up to the current index */
                    while (anchor < index) {
                        *out_index++ = *anchor++;
                    }
                }
                break;
            case POUND:
                if (c == 'i') {
                    state = POUNDI;
                } else {
                    state = SCANNING;
                }
                break;
            case POUNDI:
                if (c == 'n') {
                    state = POUNDIN;
                } else {
                    state = SCANNING;
                }
                break;
            case POUNDIN:
                if (c == 'c') {
                    state = POUNDINC;
                } else {
                    state = SCANNING;
                }
                break;
            case POUNDINC:
                if (c == 'l') {
                    state = POUNDINCL;
                } else {
                    state = SCANNING;
                }
                break;
            case POUNDINCL:
                if (c == 'u') {
                    state = POUNDINCLU;
                } else {
                    state = SCANNING;
                }
                break;
            case POUNDINCLU:
                if (c == 'd') {
                    state = POUNDINCLUD;
                } else {
                    state = SCANNING;
                }
                break;
            case POUNDINCLUD:
                if (c == 'e') {
                    state = POUNDINCLUDE;
                } else {
                    state = SCANNING;
                }
                break;
            case POUNDINCLUDE:
                /* note, this breaks if you start a block comment on the same line as an #include */
                if (c == '\n') {
                    state = BEGINNING_OF_LINE;
                    /* skip writing this line */
                    anchor = index;
                }
                break;
            case SLASH:
                if (c == '/') {
                    state = LINE_COMMENT;
                } else if (c == '*') {
                    state = BLOCK_COMMENT;
                } else if (c == '\n') {
                    state = BEGINNING_OF_LINE;
                } else {
                    state = SCANNING;
                }
                break;
            case LINE_COMMENT:
                if (c == '\n') {
                    state = BEGINNING_OF_LINE;
                    /* skip writing this line, but do include the newline... */
                    anchor = index - 1;
                }
                break;
            case BLOCK_COMMENT:
                if (c == '*') {
                    state = STAR;
                }
                break;
            case STAR:
                if (c == '/') {
                    state = SCANNING;
                    /* skip writing the block */
                    anchor = index;
                } else if (c != '*') {
                    state = BLOCK_COMMENT;
                }
                break;
            default:
                /* break out of the loop if this is reached */
                break;
            }
        }

        /* we reached the end of the buffer */
        /* write the buffer */
        if (fwrite(outbuff, out_index - outbuff, 1, outfile) != 1) {
            perror("Error writing stripped data.");
            return;
        }

        /* copy anything left on the end of inbuffer to the beginning */
        gap = 0;
        while (anchor < index) {
            inbuff[gap++] = *anchor++;
        }
        anchor = inbuff;
        index = inbuff + gap;
    }
}


int main(int argc, char *argv[])
{
    /* for debugging */
    //set_log_level(LOG_LEVEL_DEBUG);
    /* check command line */
    if (argc != 4) {
        log_msg(usage);
        return 1;
    }

    /* open the files */
    infile = fopen(argv[2], "rb");
    if (infile == NULL) {
        perror("Error opening input file.");
        return 2;
    }

    outfile = fopen(argv[3], "wb");
    if (outfile == NULL) {
        perror("Error opening output file.");
        fclose(infile);
        return 3;
    }

    /* dispatch to requested function */
    switch (argv[1] [0])
    {
    case    'c':
    case    'C':
        compress_file(infile, outfile);
        break;

    case    'd':
    case    'D':
        decompress_file(infile, outfile);
        break;

    case    's':
    case    'S':
        strip_comments_and_includes(infile, outfile);
        break;

    default:
        log_msg(usage);
    }

    /* and close the files */
    if (fclose(infile)) {
        perror("Error closing input file.");
        return 4;
    }

    if (fclose(outfile)) {
        perror("Error closing output file.");
        return 5;
    }

    return 0;
}
/* End of File */
