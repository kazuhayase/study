#include <cstdio>

const int MAX_N = 50;

int n;
int memo[MAX_N + 1];

void read();
void solve();

int main(){

  read();
  solve();
  return 0;

}

int fib(int n){
  if (n <=1 ) return n;
  if (memo[n] != 0) return memo[n];
  return memo[n] = fib (n-1) + fib (n-2);
}

void solve(){

  int ans = fib (n);

  printf ("%d\n", ans);

}

void read (){
  scanf("%d", &n);
}
