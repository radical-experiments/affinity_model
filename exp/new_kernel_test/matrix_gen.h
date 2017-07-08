#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define SCALE 10007.0

float* make_matrix(int);
void write_matrix(float*, int, char*);
float* read_matrix(int, char*);
void print_matrix(float*, int);
void diff_matrices(float*, float*, int);
