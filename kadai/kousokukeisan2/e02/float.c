#include <stdio.h>
#include <time.h>
#define N 1000000
clock_t starttime,endtime,diff;

int main(int argc, char **argv)
{
    register int i;
    register double f1,f2;
    f1=0.0;
    f2=0.001;
    starttime=clock();
    for (i=0;i<N;i++)
    {
        f1 *= f2;  // 1回目の加算
        f1 *= f2;  // 2回目の加算
        f1 *= f2;  // 3回目の加算
        f1 *= f2;  // 4回目の加算
        f1 *= f2;  // 5回目の加算
        f1 *= f2;  // 6回目の加算
        f1 *= f2;  // 7回目の加算
        f1 *= f2;  // 8回目の加算
        f1 *= f2;  // 9回目の加算
        f1 *= f2;  // 10回目の加算
        f1 *= f2;  // 11回目の加算
        f1 *= f2;  // 12回目の加算
        f1 *= f2;  // 13回目の加算
        f1 *= f2;  // 14回目の加算
        f1 *= f2;  // 15回目の加算
        f1 *= f2;  // 16回目の加算
        f1 *= f2;  // 17回目の加算
        f1 *= f2;  // 18回目の加算
        f1 *= f2;  // 19回目の加算
        f1 *= f2;  // 20回目の加算
        f1 *= f2;  // 21回目の加算
        f1 *= f2;  // 22回目の加算
        f1 *= f2;  // 23回目の加算
        f1 *= f2;  // 24回目の加算
        f1 *= f2;  // 25回目の加算
        f1 *= f2;  // 26回目の加算
        f1 *= f2;  // 27回目の加算
        f1 *= f2;  // 28回目の加算
        f1 *= f2;  // 29回目の加算
        f1 *= f2;  // 30回目の加算
        f1 *= f2;  // 31回目の加算
        f1 *= f2;  // 32回目の加算
        f1 *= f2;  // 33回目の加算
        f1 *= f2;  // 34回目の加算
        f1 *= f2;  // 35回目の加算
        f1 *= f2;  // 36回目の加算
        f1 *= f2;  // 37回目の加算
        f1 *= f2;  // 38回目の加算
        f1 *= f2;  // 39回目の加算
        f1 *= f2;  // 40回目の加算
        f1 *= f2;  // 41回目の加算
        f1 *= f2;  // 42回目の加算
        f1 *= f2;  // 43回目の加算
        f1 *= f2;  // 44回目の加算
        f1 *= f2;  // 45回目の加算
        f1 *= f2;  // 46回目の加算
        f1 *= f2;  // 47回目の加算
        f1 *= f2;  // 48回目の加算
        f1 *= f2;  // 49回目の加算
        f1 *= f2;  // 50回目の加算
        f1 *= f2;  // 51回目の加算
        f1 *= f2;  // 52回目の加算
        f1 *= f2;  // 53回目の加算
        f1 *= f2;  // 54回目の加算
        f1 *= f2;  // 55回目の加算
        f1 *= f2;  // 56回目の加算
        f1 *= f2;  // 57回目の加算
        f1 *= f2;  // 58回目の加算
        f1 *= f2;  // 59回目の加算
        f1 *= f2;  // 60回目の加算
        f1 *= f2;  // 61回目の加算
        f1 *= f2;  // 62回目の加算
        f1 *= f2;  // 63回目の加算
        f1 *= f2;  // 64回目の加算
        f1 *= f2;  // 65回目の加算
        f1 *= f2;  // 66回目の加算
        f1 *= f2;  // 67回目の加算
        f1 *= f2;  // 68回目の加算
        f1 *= f2;  // 69回目の加算
        f1 *= f2;  // 70回目の加算
        f1 *= f2;  // 71回目の加算
        f1 *= f2;  // 72回目の加算
        f1 *= f2;  // 73回目の加算
        f1 *= f2;  // 74回目の加算
        f1 *= f2;  // 75回目の加算
        f1 *= f2;  // 76回目の加算
        f1 *= f2;  // 77回目の加算
        f1 *= f2;  // 78回目の加算
        f1 *= f2;  // 79回目の加算
        f1 *= f2;  // 80回目の加算
        f1 *= f2;  // 81回目の加算
        f1 *= f2;  // 82回目の加算
        f1 *= f2;  // 83回目の加算
        f1 *= f2;  // 84回目の加算
        f1 *= f2;  // 85回目の加算
        f1 *= f2;  // 86回目の加算
        f1 *= f2;  // 87回目の加算
        f1 *= f2;  // 88回目の加算
        f1 *= f2;  // 89回目の加算
        f1 *= f2;  // 90回目の加算
        f1 *= f2;  // 91回目の加算
        f1 *= f2;  // 92回目の加算
        f1 *= f2;  // 93回目の加算
        f1 *= f2;  // 94回目の加算
        f1 *= f2;  // 95回目の加算
        f1 *= f2;  // 96回目の加算
        f1 *= f2;  // 97回目の加算
        f1 *= f2;  // 98回目の加算
        f1 *= f2;  // 99回目の加算
        f1 *= f2;  // 100回目の加算
    }
    endtime=clock();
    diff=endtime-starttime;
    printf("(elapsed,CLOCKS_PER_SEC)=(%ld,%ld)\n",diff,CLOCKS_PER_SEC);
    printf("f1=%f\n",f1);
    return 0;
}
