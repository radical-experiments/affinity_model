#include "matrix_gen.h"
#define TESTING 0


float* make_matrix(int size)
{
    srand(time(NULL));
    float* mat = (float*) malloc(size*size * sizeof(float));
    int i;
    for (i = 0; i < size*size; i++)
    {
        mat[i] = ((float)rand()) / ((float)RAND_MAX) * SCALE;
    }
    return mat;
}

void write_matrix(float* matrix, int size, char* filename)
{
    FILE *fp;
    fp = fopen(filename, "w");
    fwrite(matrix, sizeof(float), size*size, fp);
    fclose(fp);
}

float* read_matrix(int size, char* filename)
{
    float* matrix = (float*) malloc(size*size * sizeof(float));
    FILE *fp;
    fp = fopen(filename, "r");
    fread(matrix, sizeof(float), size*size, fp);
    fclose(fp);
    return matrix;
}

void print_matrix(float* matrix, int size)
{
    int i;
    for (i = 0; i < size*size; i++)
    {
        printf("%.10f ", matrix[i]);
    }
    printf("\n");
}

void diff_matrices(float* mat1, float* mat2, int size)
{
    int i;
    for (i = 0; i < size*size; i++)
    {
        if (mat1[i] != mat2[i])
        {
            printf("different\n");
            return;
        }
    }
    printf("same\n");
    return;
}

#if TESTING
int main(int argc, char** argv)
{
    if (argc != 3)
    {
        printf("you need to input the size of the square matrix you want to make, and the id of the matrix pairs, I'll make two of them\n");
        return -1;
    }
    int size = atoi(argv[1]);
    int iteration = atoi(argv[2]);
    float* mat1 = make_matrix(size);
    float* mat2 = make_matrix(size);

    //print_matrix(mat1, size);

    char mat1_name[256];
    char mat2_name[256];

    strcpy(mat1_name, "mat1_");
    strcat(mat1_name, argv[1]);
    strcat(mat1_name, "_");
    strcat(mat1_name, argv[2]);
    strcat(mat1_name, ".txt");

    strcpy(mat2_name, "mat2_");
    strcat(mat2_name, argv[1]);
    strcat(mat2_name, "_");
    strcat(mat2_name, argv[2]);
    strcat(mat2_name, ".txt");

    write_matrix(mat1, size, mat1_name);
    write_matrix(mat2, size, mat2_name);
/*
    # Testing function to read matrix, and making sure matrix written is same as matrix read
    float* new_mat1;
    float* new_mat2;
    new_mat1 = read_matrix(size, mat1_name);
    new_mat2 = read_matrix(size, mat2_name);

    print_matrix(new_mat1, size);
    diff_matrices(mat1, new_mat1, size);
    diff_matrices(mat2, new_mat2, size);
*/
    return 0;

}

#endif
