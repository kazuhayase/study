#include <stdio.h>
#include <string.h> 

#define MAX_K  100000
#define MAX_N  1000000000

int n,k;
long long a,b,c,r;
int cas,t;

// count, sequence table
int count[MAX_K + 1];
long long sequence[2 * (MAX_K + 1)];
int seq_idx;

// zero set (priority queue)
int zero[MAX_K + 1], sz = 0;

void read() {
    scanf("%d %d\n", &n, &k);
    scanf("%lld %lld %lld %lld\n", &a, &b, &c, &r);
    return;
}

void init() {
  int i;

  seq_idx = 0;
  for(i=0; i<MAX_K+1; i++){
    count[i]=0;
    sequence[i]=0; sequence[i+MAX_K+1]=0;
    zero[i]=0;
  }

}

//push to priority queue
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

//pop from priority queue
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

void print_count() {

  printf("[Count]\n");

  int i,j;
  for (i=0; i < k / 10; i++){
    printf("[%d0 .. %d9]", i, i);
    for (j=0; j < 10; j++){
      printf(" %d", count[i*10+j]);
    }
    printf("\n");
  }

  printf("[%d .. %d]", (k/10)*10, k);

  for(j = (k/10)*10; j < k+1; j++){
    printf(" %d", count[j]);
  }
  printf("\n");
}

void print_seq() {

  printf("[Sequence]\n");

  int i,j;
  for (i=0; i < seq_idx / 10; i++){
    printf("[%d0 .. %d9]", i, i);
    for (j=0; j < 10; j++){
      printf(" %lld", sequence[i*10+j]);
    }
    printf("\n");
  }

  printf("[%d .. %d]", ((seq_idx-1)/10)*10, seq_idx-1);
  for(j = ((seq_idx-1)/10)*10; j < seq_idx; j++){
    printf(" %lld", sequence[j]);
  }
  printf("\n");
}    

void ins_seq(long long x){
  if (x <= (long long) k) {
    count[(int) x]++; 
  }
  sequence[seq_idx++]=x;
}  

void step_one() {

  int i;

  // step1 pseudo random

  //m[0]=a

  ins_seq(a);

  //m[i] = (b * m[i - 1] + c) % r, 0 < i < k

  for (i=1; i<k; i++){
    ins_seq( (b * sequence[i-1] + c) % r);
  }      
}

void step_two() {
  // step2 find zero in count[]
  int i;
  for (i=0; i < k+1; i++){
    if (count[i] == 0){
      push(i);
    }
  }
}

void step_three() {
  // step3 sequence (from k to 2k+1) or (till #zero == 1)

  //make m[k] by pop
  
  ins_seq( pop() );

  //make m[k+1] to m[2k+1]

  int i;
  int mod;
  long long prev;

  for (i = k+1; i < 2*k+2; i++) {
    mod = i % (k+1);
    prev = sequence[mod];

    if (prev <= (long long) k) {
      count[(int) prev]--;
      if(count[(int) prev] == 0){
	push((int) prev);
      }
    }
    ins_seq( pop() );
  }
	
}


int main() {

  int answer;
  int i;

  scanf("%d\n", &t);

  for (cas=0; cas < t; cas++){

    init();
    read();

    step_one();
    //print_seq();

    step_two();
    //print_count();

    step_three();
    //print_seq();
    //print_count();

    int index = (n -1) % (k+1);
    
    answer = sequence [ index + k+1 ];

    printf("Case #%d: %d\n", cas+1, answer);
  }

}
