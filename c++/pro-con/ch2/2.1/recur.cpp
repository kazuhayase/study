#include <cstdio>

int n;
const int MAX_N = 50;

void read();
void solve();

int fact(int n) {
  if (n == 0) return 1;
  return n * fact(n-1);
}

int memo[MAX_N +1];

int fib(int n){
  if (n <= 1) return n;
  if (memo[n] != 0) return memo[n];
  return fib(n-1) + fib(n-2);
}

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d", &n);
}

void solve(){

  int ans=0;
  ans = fact(n);
  printf("fact = %d\n", ans);

  printf("fib = %d\n", fib(n));

}
