#include <stdio.h>

static unsigned long LUT[0x100] = {0, };

unsigned long digest(unsigned char *string, unsigned long len)
{
    unsigned long i = 0;
    unsigned long hash = 0xFFFFFFFF;
    unsigned long ebx = 0, eax = 0;
    for (; i < len; ++i) {
        eax = (unsigned long)(string[i]);
        eax ^= (hash & 0xFF);
        ebx = LUT[eax];
        hash >>= 8;
        hash ^= ebx;
    }
    return ~hash;
}

int main(int argc, char *argv[])
{
    unsigned long i = 0, j = 0, k = 0;
    unsigned char data[0xa0] = {0, };
    
    unsigned long guess;
    
    FILE *fp = NULL;

    if ((fp = fopen("dataset.bin", "rb")) == NULL) {
        return 1;
    }

    fread(data, 1, 0xa0, fp);

     /* Generate a look up table (LUT) */
    for (; i < 0x100; ++i) {
        j = i;
        for (k = 0; k < 8; ++k) {
            if ((j & 1) == 0) {
                j >>= 1;
            } else {
                j >>= 1;
                j ^= 0xEDB88320;
            }
        }
        LUT[i] = j;
    }
    for (guess = 0x400000; guess <= 0x500000; ++guess) {
        *(unsigned long *)(data + 80) = guess;
        if (digest(data, 0xa0) == 0xa640740e) {
            printf("%08lX\n", guess);
        }
    }
    return 0;
}
