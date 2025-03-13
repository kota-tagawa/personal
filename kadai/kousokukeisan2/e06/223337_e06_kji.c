#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 4096

// ループ順序変更
void MatrixMul(double **A, double **B, double **C)
{
    int i,j,k;
    double tmp;

    for (i=0;i<SIZE;i++){
        for (j=i+1;j<SIZE;j++){
            tmp     = B[j][i];
            B[j][i] = B[i][j];
            B[i][j] = tmp;
        }
    }

    for (k=0; k<SIZE; k++){
        for (j=0; j<SIZE; j++){
            for (i=0; i<SIZE; i++)
                C[i][j] += A[i][k]*B[j][k];
        }
    }
}

int main(int argc, char *argv[]){
    int i,j;
    double **a,**b,**c;
    clock_t ts,te;
    clock_t d1,d2,d3;

    printf("Serial Program. (2d ver.)\n");
    printf("Matrix Size: %d X %d.\n",SIZE,SIZE);

    ts = clock();
//---------------------
    a=(double**)malloc(SIZE*sizeof(double*));
    a[0] = (double*)malloc(SIZE*SIZE*sizeof(double));

    b=(double**)malloc(SIZE*sizeof(double*));
    b[0] = (double*)malloc(SIZE*SIZE*sizeof(double));

    c=(double**)malloc(SIZE*sizeof(double*));
    c[0] = (double*)malloc(SIZE*SIZE*sizeof(double));

    for(i=1;i<SIZE;i++){
        a[i]  = a[i-1]  + SIZE;
        b[i]  = b[i-1]  + SIZE;
        c[i]  = c[i-1]  + SIZE;
    }
    d1 = clock();
//---------------------
    srand(10);

    for(i=0; i<SIZE; i++){
        for(j=0; j<SIZE; j++){
            a[i][j] = rand()/(double)RAND_MAX;
            b[i][j] = rand()/(double)RAND_MAX;
            c[i][j] = 0.0;
        }
    }
    d2 = clock();
//---------------------
    MatrixMul(a,b,c);
    d3 = clock();
//---------------------
    printf("Result:\n");
    printf("c[0][0]= %.15e ... c[%d][0]=%.15e\n",c[0][0],SIZE-1,c[SIZE-1][0]);
    printf("c[0][1]= %.15e ... c[%d][1]=%.15e\n",c[0][1],SIZE-1,c[SIZE-1][1]);
    printf("c[0][2]= %.15e ... c[%d][2]=%.15e\n",c[0][2],SIZE-1,c[SIZE-1][2]);
    printf("c[0][3]= %.15e ... c[%d][3]=%.15e\n",c[0][3],SIZE-1,c[SIZE-1][3]);
    printf(".......\n");
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n",SIZE-4,c[0][SIZE-4],SIZE-1,SIZE-4,c[SIZE-1][SIZE-4]);
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n",SIZE-3,c[0][SIZE-3],SIZE-1,SIZE-3,c[SIZE-1][SIZE-3]);
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n",SIZE-2,c[0][SIZE-2],SIZE-1,SIZE-2,c[SIZE-1][SIZE-2]);
    printf("c[0][%d]= %.15e ... c[%d][%d]=%.15e\n",SIZE-1,c[0][SIZE-1],SIZE-1,SIZE-1,c[SIZE-1][SIZE-1]);

    te = clock();

    printf("\nTotal Time : %f [sec]\n", (float)(te-ts)/CLOCKS_PER_SEC);
    printf("Time of Allocation           : %f [sec]\n", (float)(d1-ts)/CLOCKS_PER_SEC);
    printf("Time of Initialization       : %f [sec]\n", (float)(d2-d1)/CLOCKS_PER_SEC);
    printf("Time of Operation for Matrix : %f [sec]\n", (float)(d3-d2)/CLOCKS_PER_SEC);
//---------------------
    free(a[0]);  free(a);
    free(b[0]);  free(b);
    free(c[0]);  free(c);
//---------------------
    return 0;
}
