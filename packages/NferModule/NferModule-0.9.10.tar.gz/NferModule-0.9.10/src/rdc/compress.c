/*
 * COMPRS.C - Ross Data Compression (RDC)
 *            compress function
 *
 * Written by Ed Ross, 1/92
 *
 * compress inbuff_len bytes of inbuff into outbuff
 * using hash_len entries in hash_tbl.
 *
 * return length of outbuff, or "0 - inbuff_len"
 * if inbuff could not be compressed.
 *
 * Updated and documented by smk July 2018
 */

#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* use the logging capability from nfer */
#include "log.h"
#include "rdc.h"

static int rdc_compress(uint8_t *inbuff, uint16_t inbuff_len, uint8_t *outbuff, uint8_t *hash_tbl[], uint16_t hash_len) {
    uint8_t   *input_index = inbuff;
    uint8_t   *inbuff_end = inbuff + inbuff_len;
    uint8_t   *anchor;
    uint8_t   *pattern_index;
    uint16_t  count;
    uint16_t  gap;
    uint16_t  c;
    uint16_t  hash;
    uint16_t  *control_index = (uint16_t *) outbuff;
    uint16_t  control_bits = 0;
    uint16_t  control_count = 0;

    uint8_t   *out_idx = outbuff + sizeof(uint16_t);
    uint8_t   *outbuff_end = outbuff + (inbuff_len - 48);

    /* skip the compression for a small buffer */
    if (inbuff_len <= 18)
    {
        filter_log_msg(LOG_LEVEL_INFO, "Skipping compression due to small buffer size.\n");
        memcpy(outbuff, inbuff, inbuff_len);
        return 0 - inbuff_len;
    }

    /* adjust # hash entries so hash algorithm can use 'and' instead of 'mod' */
    hash_len--;

    /* scan thru inbuff */
    while (input_index < inbuff_end)
    {
        /* make room for the control bits and check for outbuff overflow */
        if (control_count++ == 16)
        {
            *control_index = control_bits;
            control_count = 1;
            control_index = (uint16_t *) out_idx;
            out_idx += 2;

            if (out_idx > outbuff_end)
            {
                filter_log_msg(LOG_LEVEL_ERROR, "Compression overflowed the output buffer!\n");
                /* the original code then went ahead and wrote to the output buffer... */
                //memcpy(outbuff, inbuff, inbuff_len);
                return 0 - inbuff_len;
            }
        }

        /* look for rle */
        /* set the anchor so we can reload the input_index if no rle is found */
        anchor = input_index;
        c = *input_index++;

        /* this tries to find consecutive identical characters */
        filter_log_msg(LOG_LEVEL_DEBUG, "Looking for match for run-length-encoding for char '%c'.\n", c);
        while (input_index < inbuff_end
                && *input_index == c
                && (input_index - anchor) < 4114) {
            input_index++;
        }

        /* store compression code if character is repeated more than 2 times */
        count = input_index - anchor;
        if (count > 2)
        {
            filter_log_msg(LOG_LEVEL_DEBUG, "Found RLE for '%c' of length %d.", c, count);
            if (count <= 18)         /* short rle */
            {
                /* this is an optimization, since the count must always be at least 3 */
                *out_idx++ = count - 3;
                *out_idx++ = c;
            }
            else                   /* long rle */
            {
                /* similarly, the count for a long rle must always be at least 19 */
                count -= 19;
                *out_idx++ = 16 + (count & 0x0F);
                *out_idx++ = count >> 4;
                *out_idx++ = c;
            }
            control_bits = (control_bits << 1) | 1;

            continue;
        }

        /* look for pattern if 2 or more characters remain in the input buffer */
        /* reload the anchor, since we didn't find an rle */
        input_index = anchor;

        filter_log_msg(LOG_LEVEL_DEBUG, "No RLE, looking for pattern.\n");
        if ((inbuff_end - input_index) > 2)
        {
            /* locate offset of possible pattern in sliding dictionary */

            hash = ((((input_index[0] & 15) << 8) | input_index[1]) ^
                    ((input_index[0] >> 4) | (input_index[2] << 4)))
                & hash_len;

            /* get the start of the last time you saw a pattern with this hash from the hash table */
            pattern_index = hash_tbl[hash];
            /* then store this index back to the hash table */
            hash_tbl[hash] = input_index;

            /* compare characters if we're within 4098 bytes */
            gap = input_index - pattern_index;
            if (pattern_index != NULL && gap <= 4098)
            {
                /* increment the input_index and pattern_index while they are equal */
                while (input_index < inbuff_end
                        && pattern_index < anchor && *pattern_index == *input_index
                        && (input_index - anchor) < 271)
                {
                    input_index++;
                    pattern_index++;
                }

                /* store pattern if it is more than 2 characters */
                count = input_index - anchor;
                if (count > 2)
                {
                    gap -= 3;

                    if (count <= 15)          /* short pattern */
                    {
                        *out_idx++ = (count << 4) + (gap & 0x0F);
                        *out_idx++ = gap >> 4;
                    }
                    else                    /* long pattern */
                    {
                        *out_idx++ = 32 + (gap & 0x0F);
                        *out_idx++ = gap >> 4;
                        *out_idx++ = count - 16;
                    }

                    control_bits = (control_bits << 1) | 1;

                    continue;
                }
            }
        }

        /* can't compress this character so copy it to outbuff */
        filter_log_msg(LOG_LEVEL_DEBUG, "Can't compress char '%c', so copying directly.\n", c);
        *out_idx++ = c;
        input_index = ++anchor;
        control_bits <<= 1;
    }

    /* save last load of control bits */

    control_bits <<= (16 - control_count);
    *control_index = control_bits;

    /* and return size of compressed buffer */

    return out_idx - outbuff;
}

/*--- compress infile to outfile ---*/

rdc_error_code compress_file(FILE *infile, FILE *outfile) {
    int bytes_read;
    int compress_len;
    uint8_t inbuff[RDC_IO_BUFFER_LENGTH];     /* io buffers */
    uint8_t outbuff[RDC_IO_BUFFER_LENGTH];
    uint8_t *hash_tbl[RDC_HASH_TABLE_LENGTH];  /* hash table */

    /* read infile BUFF_LEN bytes at a time */
    while ((bytes_read = fread(inbuff, 1, RDC_IO_BUFFER_LENGTH, infile)) > 0) {
        /* make sure the hash table is cleared */
        memset(hash_tbl, 0, sizeof(uint8_t *) * RDC_HASH_TABLE_LENGTH);

        /* compress this load of bytes */
        compress_len = rdc_compress(inbuff, bytes_read, outbuff, hash_tbl, RDC_HASH_TABLE_LENGTH);

        /* write length of compressed buffer */
        if (fwrite(&compress_len, sizeof(int), 1, outfile) != 1) {
            filter_log_msg(LOG_LEVEL_ERROR, "Error writing block length.\n");
            return ERROR_BLOCK_LENGTH;
        }

        /*check for negative length indicating the buffer could not be compressed */
        if (compress_len < 0) {
            compress_len = 0 - compress_len;
        }

        /* write the buffer */
        if (fwrite(outbuff, compress_len, 1, outfile) != 1) {
            filter_log_msg(LOG_LEVEL_ERROR, "Error writing compressed data.\n");
            return ERROR_WRITE_COMPRESSED;
        }

        /* we're done if less than full buffer was read */
        if (bytes_read != RDC_IO_BUFFER_LENGTH) {
            break;
        }
    }

    /* add trailer to indicate end of file */

    compress_len = 0;

    if (fwrite(&compress_len, sizeof(int), 1, outfile) != 1) {
        filter_log_msg(LOG_LEVEL_ERROR, "Error writing trailer.\n");
        return ERROR_TRAILER;
    }

    return NO_ERROR;
}
/* End of File */
