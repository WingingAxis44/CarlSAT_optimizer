#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <assert.h>

#define NHARD	    30
#define SEED	123456

int main (int argc, char** argv) {

  int seed  = SEED;
  int nHard = NHARD;

  if (argc > 1) nHard = atoi (argv[1]);
  if (argc > 2) seed  = atoi (argv[2]);

  int nSoft = nHard * sqrt(nHard);

  srand (seed);

  int **hard;
  int  *size;
  int  *card;
  int  *mark;
  int *count;

  hard = (int**) malloc (sizeof (int*) * nHard);
  size = (int *) malloc (sizeof (int ) * nHard);
  card = (int *) malloc (sizeof (int ) * nHard);

  int i, j, sum = 0;
  int l = (int) log2(nHard);
  for (i = 0; i < nHard; i++) {
    size[i] = rand() % nHard + 6;
    int m = (int) log2(log2(size[i]) + 2) + 2;
    card[i] =  rand() % (rand() % m + 1) + 1;
    sum += size[i];
  }

  mark  = (int *) malloc (sizeof (int) * (sum+1));
  count = (int *) malloc (sizeof (int) * (sum+1));
  for (i = 0; i <= sum; i++) mark[i] = count[i] = 0;

  printf ("p wcard %i %i 1000\n", sum, nSoft + nHard);

  for (i = 1; i <= nSoft; i++) {
    printf ("%i ", rand() % 800 + 10); // print the weight
    int full = 0;
    do {
      int lit;
      do {
        lit = rand() % sum + 1;
      }
      while (count[lit] > (rand() % 10));
      assert (lit <= sum);

      if (mark[lit] != i) {
        mark[lit] = i;
        count[lit]++;
        printf ("%i ", lit);
      }
      full += rand() % (rand() % (nHard) + 1) + 1;
    }
    while (full < nHard);
    printf ("0\n");
  }

  int tmp = 1;
  for (i = 0; i < nHard; i++) {
    printf ("1000 ");
    for (j = 0; j < size[i]; j++)
      printf ("%i ", tmp++);
    printf ("<= %i\n", card[i]);
  }


}
