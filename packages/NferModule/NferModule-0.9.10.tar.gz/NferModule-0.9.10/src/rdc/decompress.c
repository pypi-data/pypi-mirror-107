/*
 * DECOMPRS.C - Ross Data Compression (RDC)
 *              decompress function
 *
 * Written by Ed Ross, 1/92
 *
 * decompress inbuff_len bytes of inbuff into outbuff.
 * return length of outbuff.
 *
 * Updated and documented by smk July 2018.
 */

#include <stdint.h>
#include <stdio.h>
#include <string.h>

/* use the logging capability from nfer */
#include "log.h"
#include "rdc.h"


static int rdc_decompress(uint8_t *inbuff, uint16_t inbuff_len, uint8_t *outbuff) {
    uint16_t   control_bits = 0;
    uint16_t   control_mask = 0;
    uint8_t    *inbuff_index = inbuff;
    uint8_t    *outbuff_index = outbuff;
    uint8_t    *inbuff_end = inbuff + inbuff_len;
    uint16_t   command;
    uint16_t   count;
    uint16_t   offset;

    /* process each item in inbuff */

    while (inbuff_index < inbuff_end)
    {
        /* get new load of control bits if needed */
        /* this serves to count the iterations while also updating the mask */
        if ((control_mask >>= 1) == 0)
        {
            control_bits = * (uint16_t *) inbuff_index;
            inbuff_index += 2;
            control_mask = 0x8000;
        }

        /* just copy this char if control bit is zero */
        /* nothing was compressed, just copy a byte and continue */
        if ((control_bits & control_mask) == 0)
        {
            *outbuff_index++ = *inbuff_index++;

            continue;
        }

        /* undo the compression code */
        /* the command is the high nybble and the count is the low nybble */
        command = (*inbuff_index >> 4) & 0x0F;
        count = *inbuff_index++ & 0x0F;

        switch (command)
        {
        case 0:     /* short rle */
            /* count is always at least 3, so to optimize, 3 was subtracted from the count */
            count += 3;
            memset(outbuff_index, *inbuff_index++, count);
            outbuff_index += count;
            break;

        case 1:     /* long /rle */
            count += (*inbuff_index++ << 4);
            /* ditto for long rle but 19 instead of 3 */
            count += 19;
            memset(outbuff_index, *inbuff_index++, count);
            outbuff_index += count;
            break;

        case 2:     /* long pattern */
            /* offset gets the relative address of the hash table entry */
            offset = count + 3;
            offset += (*inbuff_index++ << 4);
            count = *inbuff_index++;
            count += 16;
            memcpy(outbuff_index, outbuff_index - offset, count);
            outbuff_index += count;
            break;

        default:    /* short pattern */
            offset = count + 3;
            offset += (*inbuff_index++ << 4);
            memcpy(outbuff_index, outbuff_index - offset, command);
            outbuff_index += command;
            break;
        }
    }

    /* return length of decompressed buffer */

    return outbuff_index - outbuff;
}

/*--- decompress infile to outfile ---*/
rdc_error_code decompress_file(FILE *infile, FILE *outfile) {
    int block_len;
    int decomp_len;
    uint8_t inbuff[RDC_IO_BUFFER_LENGTH];     /* io buffers */
    uint8_t outbuff[RDC_IO_BUFFER_LENGTH];

    /* read infile BUFF_LEN bytes at a time */
    for (;;)
    {
        if (fread(&block_len, sizeof(int), 1, infile) != 1) {
            filter_log_msg(LOG_LEVEL_ERROR, "Can't read block length.\n");
            return ERROR_BLOCK_LENGTH;
        }

        /* check for end-of-file flag */
        if (block_len == 0) {
            break;
        }

        if (block_len < 0)  /* copy uncompressed chars */
        {
            decomp_len = 0 - block_len;
            if (fread(outbuff, decomp_len, 1, infile) != 1) {
                filter_log_msg(LOG_LEVEL_ERROR, "Can't read uncompressed block.\n");
                return ERROR_READ_UNCOMPRESSED;
            }
        }
        else                /* decompress this buffer */
        {
            if (fread(inbuff, block_len, 1, infile) != 1) {
                filter_log_msg(LOG_LEVEL_ERROR, "Can't read compressed block.\n");
                return ERROR_READ_COMPRESSED;
            }

            decomp_len = rdc_decompress(inbuff, block_len, outbuff);
        }

        /* and write this buffer to outfile */
        if (fwrite(outbuff, decomp_len, 1, outfile) != 1) {
            filter_log_msg(LOG_LEVEL_ERROR, "Error writing uncompressed data.\n");
            return ERROR_WRITE_UNCOMPRESSED;
        }
    }

    /* everything completed */
    return NO_ERROR;
}

/*--- decompress char array to outfile ---*/
rdc_error_code decompress_array_to_file(uint8_t inbuff[], FILE *outfile) {
    int block_len;
    int decomp_len;
    uint8_t *index = inbuff;
    uint8_t outbuff[RDC_IO_BUFFER_LENGTH];

    /* we still have to loop because the block length is mixed in */
    for (;;)
    {
        block_len = *((int*)index); /* get the first word */
        index += sizeof(int);       /* update the index */

        /* check for end-of-file flag */
        if (block_len == 0) {
            break;
        }

        if (block_len < 0)  /* copy uncompressed chars */
        {
            decomp_len = 0 - block_len;
            /* we know there is enough room, since the buffers were the same size */
            memcpy(outbuff, index, decomp_len);
            /* update the index */
            index += decomp_len;
        }
        else                /* decompress this buffer */
        {
            decomp_len = rdc_decompress(index, block_len, outbuff);
            /* update the index */
            index += block_len;
        }

        /* and write this buffer to outfile */
        if (fwrite(outbuff, decomp_len, 1, outfile) != 1) {
            filter_log_msg(LOG_LEVEL_ERROR, "Error writing uncompressed data.\n");
            return ERROR_WRITE_UNCOMPRESSED;
        }
    }

    /* everything completed */
    return NO_ERROR;
}
/* End of File */
