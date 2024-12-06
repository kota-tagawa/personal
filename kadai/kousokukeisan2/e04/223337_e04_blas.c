#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mkl.h>

#define SIZE 4096

int main(int argc, char *argv[]){
    int i,j;
    double *a, *b, *c;
    clock_t ts, te;
    clock_t d1, d2, d3;

    printf("BLAS Program (1d ver.)\n");
    printf("Matrix Size: %d X %d.\n", SIZE, SIZE);

    ts = clock();
//---------------------
    a = (double*)malloc(SIZE * SIZE * sizeof(double));
    b = (double*)malloc(SIZE * SIZE * sizeof(double));
    c = (double*)malloc(SIZE * SIZE * sizeof(double));
    d1 = clock();
//---------------------
    srand(10);

    for(i = 0; i < SIZE; i++){
        for(j = 0; j < SIZE; j++){
            a[i * SIZE + j] = rand() / (double)RAND_MAX;
            b[i * SIZE + j] = rand() / (double)RAND_MAX;
            c[i * SIZE + j] = 0.0;
        }
    }
    d2 = clock();
//---------------------
    // BLASの行列積関数を呼び出し
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, SIZE, SIZE, SIZE, 
                1.0, a, SIZE, b, SIZE, 0.0, c, SIZE);
    d3 = clock();
//---------------------
    printf("Result:\n");
    printf("c[0][0]= %.15e ... c[%d][0]=%.15e\n", c[0], SIZE-1, c[(SIZE-1) * SIZE + 0]);
    printf("c[0][1]= %.15e ... c[%d][1]=%.15e\n", c[1], SIZE-1, c[(SIZE-1) * SIZE + 1]);
    printf("c[0][2]= %.15e ... c[%d][2]=%.15e\n", c[2], SIZE-1, c[(SIZE-1) * SIZE + 2]);
    printf("c[0][3]= %.15e ... c[%d][3]=%.15e\n", c[3], SIZE-1, c[(SIZE-1) * SIZE + 3]);
    printf(".......\n");
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n", SIZE-4, c[SIZE-4], SIZE-1, SIZE-4, c[(SIZE-1) * SIZE + SIZE-4]);
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n", SIZE-3, c[SIZE-3], SIZE-1, SIZE-3, c[(SIZE-1) * SIZE + SIZE-3]);
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n", SIZE-2, c[SIZE-2], SIZE-1, SIZE-2, c[(SIZE-1) * SIZE + SIZE-2]);
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n", SIZE-1, c[SIZE-1], SIZE-1, SIZE-1, c[(SIZE-1) * SIZE + SIZE-1]);

    te = clock();

    printf("\nTotal Time : %f [sec]\n", (float)(te-ts)/CLOCKS_PER_SEC);
    printf("Time of Allocation           : %f [sec]\n", (float)(d1-ts)/CLOCKS_PER_SEC);
    printf("Time of Initialization       : %f [sec]\n", (float)(d2-d1)/CLOCKS_PER_SEC);
    printf("Time of Operation for Matrix : %f [sec]\n", (float)(d3-d2)/CLOCKS_PER_SEC);
//---------------------
    free(a);
    free(b);
    free(c);
//---------------------
    return 0;
}
