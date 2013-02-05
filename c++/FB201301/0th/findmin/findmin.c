#include <stdio.h>
#include <string.h> 

#define MAX_K  100000
#define MAX_N  1000000000

int main() {

  int cas,t;

  scanf("%d\n", &t);

  for (cas=0; cas < t; cas++){

    int n,k;
    long long a,b,c,r;

    scanf("%d %d\n", &n, &k);
    scanf("%lld %lld %lld %lld\n", &a, &b, &c, &r);

    int value[MAX_K + 1];
    long long sequence[MAX_K + 1];
    int answer;
    int i;
    long long m;

    for(i=0; i<MAX_K+1; i++){
      value[i]=0;
      sequence[i]=0;
    }

    // step1 pseudo random

    m = a; 
    if (m <= k) value[m]++; 
    sequence[0]=m;

    for (i=1; i<k; i++){
      m = (b * m + c) % r;
      if (m <= k) value[m]++; 
      sequence[i]=m;
    }      

    /*
    printf("sequence\n");

    for(i=0; i<k; i++){
      printf("%d:%d, ", i, sequence[i]);
    }

    printf("\nvalue\n");

    for(i=0; i<k+1; i++){
      printf("%d:%d, ", i, value[i]);
    }

    */

    // step2 find zero in value[]

    int zero[MAX_K + 1], sz = 0;

    for(i=0; i < MAX_K + 1; i++){
      zero[i]=0;
    }


    void push(int x) {
      int i = sz++;

      while ( i > 0 ) {
	int p = (i-1) / 2;
	if (zero[p] <= x) break;
	zero[i] = zero[p];
	i = p;
      }
      zero[i]=x;
    }

    int pop(){
      int ret = zero[0];
      int x = zero[--sz];
      int i = 0;
      while (i * 2 + 1 < sz) {
	int a =i * 2 + 1, b = i * 2 +2;
	if (b < sz && zero[b] < zero[a]) a = b;
	if (zero[a] >= x) break;
	zero[i] = zero[a];
	i = a;
      }
      zero[i] = x;
      return ret;
    }

    for (i=0; i<k+1; i++){
      if (value[i] == 0){
	push(i);
      }
    }      

    /*
    printf("\nzero\n");
    for(i=0; i<k+1; i++){
      printf("%d:%d ", i, zero[i]);
    }
    printf("\nsz=%d\n",sz);
    */

    // at 'k'

    int xk;
    xk = pop();
    sequence[k] = xk;
    value[xk]++;

    int seq = 0; // start at 'k+1'
    int prev, next;

    while (sz > 0) {
    //while (seq < k) {
      prev = sequence[seq];
      next = pop();
      sequence[seq] = next;
      value[next]++;
      seq++;

      if (prev <= k){
	value[prev]--;
	if(value[prev] == 0){
	  push(prev);
	}
      }
    }

    /*
    printf("sequence\n");

    for(i=0; i<k+1; i++){
      printf("%d:%d, ", i, sequence[i]);
    }

    printf("\nvalue\n");

    for(i=0; i<k+1; i++){
      printf("%d:%d, ", i, value[i]);
    }

    printf("\nzero\n");
    for(i=0; i<k+1; i++){
      printf("%d:%d ", i, zero[i]);
    }
    printf("\nsz=%d\n",sz);
    printf("seq=%d\n",seq);

    */

    int index = (n -1) % (k+1);
    
    answer = sequence [ index ];

    printf("Case #%d: %d\n", cas+1, answer);
  }

}
