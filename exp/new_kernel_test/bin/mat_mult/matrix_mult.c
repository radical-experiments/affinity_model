#include <stdlib.h>
#include <stdio.h>
#include "matrix_gen.h"


void mat_mult(float* mat1, float* mat2, float* out_mat, int size)
{
    int i, j, k;
    for (i = 0; i < size; i++)
    {
        for (j = 0; j < size; j++)
        {
            for (k = 0; k < size; k++)
            {
                out_mat[i*size + j] = mat1[i*size + k] * mat2[k*size + j];
            }
            //out_mat[i*size + j] /= 1000.0;
        }
    }
}

int main(int argc, char** argv)
{
    if (argc != 4)
    {
        printf("Input the file name of two square matrices to multiply and their size\n");
        return -1;
    }
    char* mat1_name = argv[1];
    char* mat2_name = argv[2];
    int size = atoi(argv[3]);

    float* mat1 = read_matrix(size, mat1_name);
    float* mat2 = read_matrix(size, mat2_name);
    float* out_mat = (float*) calloc(size*size, sizeof(float));

    mat_mult(mat1, mat2, out_mat, size);

    return 0;
}
