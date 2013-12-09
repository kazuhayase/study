#include <cstdio>
#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>

using namespace std;
typedef unsigned long long ull;

int T;
const int MAX_T = 20;

string L;
ull N;

void read_T();
void read(int t);
void solve(int t);

int main(){
  read_T();
  for(int i=0; i<T; i++){
    read(i);
    solve(i);
  }
  return 0;
}

void read_T(){
  cin >> T;
  fprintf(stderr, "T=%d\n", T);
}

void read(int t){

  //cin >> L[i] >> N[i];
  //fprintf(stderr, "L[%d]; %s, N[%d]; %llu\n", i, L[i], i, N[i]);

  cin >> L >> N;
  //fprintf(stderr, "L[%d]; %s, N[%d]; %llu\n", t, L, t, N);
  cerr << L << " " << N << "\n";

}

void solve(int t){

  printf("Case #%d: ", t+1);

  const int MAX_LABEL = 51;
  int A[MAX_LABEL];
  int l = L.size();

  int len=1;
  ull M=l;
  while(N >= M*l+l){
    M = M*(unsigned long long) l +l; 
    len++;
  }

  fprintf(stderr,"M=%llu, len=%d, l=%d\n", M, len,l);

  if(N == M){
    for(int i=0; i<len; i++){
      printf("%c", L[L.size()-1]);
    }    
  } else {
    ull rest = N - M - 1;
    fprintf(stderr,"rest=%llu\n", rest);
    int i=0;
    while(rest>0){
      A[i] = rest % (unsigned long long) l;
      rest = (rest - (unsigned long long) A[i]) / (unsigned long long) l;
      i++;
    }

    fprintf(stderr,"i=%d\n", i);

    if(i<=len){
      for(int j=0; j<=len-i; j++){
	printf("%c", L[0]);
      }
    }

    while(i>0){
      printf("%c", L[A[--i]]);
    }
  }
  printf("\n");
}
