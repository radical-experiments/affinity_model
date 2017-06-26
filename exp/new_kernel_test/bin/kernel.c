#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>


int main(int argc, char** argv)
{
    
    if (argc != 2)
    {
        printf("you need to input the number of iterations you want run\n");
        return -1;
    }
/*
    int pid = getpid();
    printf("My pid is %d\n", pid);

    long long int iters = atoll(argv[1]);
    printf("Running for %lld iterations\n", iters);
    if (!iters) {
        printf("Not running iterations, leaving now\n");
        return 0;
    } 
    else 
*/
    {
        long int iters = atoll(argv[1]);
        long int i;
        for (i = 0; i < iters; i++) 
        {
        __asm__ __volatile__
            (
            "addl %%eax, %%eax \n\t"
            "addl %%ebx, %%ebx \n\t"
            "addl %%ecx, %%ecx \n\t"
            "addl %%edx, %%edx \n\t"
            : /* outputs */
            : /* inputs */
            : /* clobbered */ "eax", "ebx", "ecx", "edx"
            );
        }
    }

    return 0;
}
