#include <cstdio>
#include <algorithm>
#include <queue>

using namespace std;

typedef long long ll;
int const MAX_N = 1000000;
int prime[MAX_N]; // i-th prime number below 1000000
bool is_prime[MAX_N + 1];
int p; // number of prime numbers

//エラトステネスのふるい

// number of primes below N
int sieve(int n){
  int p = 0;
  for (int i=0; i<=n; i++) is_prime[i]=true;
  is_prime[0] = is_prime[1] = false;
  for (int i=2; i<=n; i++){
    if (is_prime[i]){
      prime[p++] = i;
      for (int j=2*i; j<=n; j+=i) is_prime[j] = false;
    }
  }
  return p;
}


/// Union-Find-Tree

int par[MAX_N];
int Rank[MAX_N];

void init_union_find(int n){
  for(int i=0; i<n; i++){
    par[i]=i;
    Rank[i]=0;
  }
}

int find(int x){
  if (par[x] == x){
    return x;
  } else {
    return par[x] = find(par[x]);
  }
}
void unite(int x, int y) {
  x = find(x);
  y = find(y);

  if (x == y) return;

  if (Rank[x] < Rank[y]){
    par[x] = y;
  } else {
    par[y] = x;
    if (Rank[x] == Rank[y]) Rank[x]++;
  }
}

bool same(int x, int y){
  return find(x) == find(y);
}


// INPUT
ll A, B, P;

void solve(){
  int len = B - A + 1;
  init_union_find(len);

  for(int i=0; i<p; i++){
    if (prime[i] >= P){
      // minimum multiple of prime[i] more than or equal to A
      ll start = ( A + prime[i] - 1) / prime[i] * prime[i];
      // maximum multiple of prime[i] less than or equal to B
      ll end = B / prime[i] * prime[i];

      for (ll j = start; j <= end; j += prime[i]){
	unite(start - A, j - A);
      }
    }
  }
  int res = 0;
  for (ll i = A; i <= B; i++){
    if(find(i - A) == i - A) res++;
  }
  printf("%d\n", res);
}

int main(){
  p = sieve(MAX_N);

  A = 10, B = 20, P = 5;
  solve();

  A = 10, B = 20, P = 3;
  solve();
}
