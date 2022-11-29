#include <stdio.h>
#include <stdlib.h>

int main (int argc, char **argv) {

  int tmp, lit, size = 0;
  int array[10000];
  int units = 0;
  int nVar, nCls, max;

  FILE *wcard = fopen (argv[1], "r");
  tmp = fscanf (wcard, " c sum of units = %i ", &units);
  tmp = fscanf (wcard, " p wcard %i %i %i ", &nVar, &nCls, &max);

  printf("Minimize\nobj: ");

  int count = 0;
  do {
    tmp = fscanf (wcard, " %i ", &lit);
    if (tmp == 1) {
      array[size++] = lit;

      if (lit == 0) {
        if (count != 0) printf (" + ");
        count++;
        printf ("%i p%i", array[0], count);
        size = 0;
      }
    }
    else {
      tmp = fscanf (wcard, " <= %i ", &lit);
      if (tmp == 1) size = 0;
    }
  }
  while (tmp != EOF);
  printf ("\n\n");

  fclose (wcard);

  wcard = fopen (argv[1], "r");
  tmp = fscanf (wcard, " c sum of units = %i ", &units);
  tmp = fscanf (wcard, " p wcard %i %i %i ", &nVar, &nCls, &max);

  printf ("Subject To\n");
  for (int i = 1; i <= nVar; i++)
    printf ("a%i - r%i <= 0\n", i, i);

  count = 0;
  do {
    tmp = fscanf (wcard, " %i ", &lit);
    if (tmp == 1) {
      array[size++] = lit;

      if (lit == 0) {
        count++;
        for (int i = 1; i < size - 1; i++)
          printf ("a%i + ", array[i]);
        printf ("p%i >= 1\n", count);
        size = 0;
      }
    }
    else {
      tmp = fscanf (wcard, " <= %i ", &lit);

      if (tmp == 1) {
        for (int i = 1; i < size - 1; i++)
          printf ("r%i + ", array[i]);
        printf ("r%i <= %i\n", array[size-1], lit);
        size = 0;
      }
    }
  }
  while (tmp != EOF);

  fclose (wcard);

  printf ("Bounds\n");

  printf ("bin\n");
  for (int i = 1; i <= nVar; i++)
    printf ("r%i\n", i);
  printf("\n");

  printf ("semi\n");
  for (int i = 1; i <= nVar; i++)
    printf ("0 <= a%i <= 1\n", i);
  for (int i = 1; i <= count; i++)
    printf ("0 <= p%i <= 1\n", i);
  printf("\n");

  printf ("End\n");

}
