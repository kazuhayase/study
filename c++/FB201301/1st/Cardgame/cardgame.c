#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_N  100000
#define MOD    1000000007

typedef long long ll;

int n,k,t,cas;
long a[MAX_N];

ll sum, cmb;

int long_sort_cmp(const void* a, const void* b){
  return  *(long *) b - *(long *) a;
}

void read() {
    scanf("%d %d\n", &n, &k);

    int i;

    for (i=0; i<n; i++){
      scanf("%ld", &a[i]);
    }

    return;
}

void init() {
  int i;

  sum=0, cmb=1;

  for(i=0; i<MAX_N+1; i++){
    a[i]=0;
  }

}

void print_a() {

  printf("[A]\n");

  int i,j;
  for (i=0; i < n; i++){
    printf("%ld", a[i]);
  }
  printf("\n");
}

int main() {

  int i;

  scanf("%d\n", &t);

  for (cas=0; cas < t; cas++){

    init();
    read();

    //print_a();

    qsort(&a[0], n, sizeof(&a[0]), long_sort_cmp);

    //print_a();

    for (i=0; i < n-k+1; i++){
      if (i>0) cmb = (cmb + cmb * (k-1) / i) % MOD;
      sum = (sum + a[n-k-i] * cmb) % MOD;
    }
    printf("Case #%d: %lld\n", cas+1, sum);
  }

}
