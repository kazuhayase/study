#include <cstdio>
#include <algorithm>
#include <queue>

using namespace std;

const int MAX_N = 20000;

int par[MAX_N];
int Rank[MAX_N];

void init(int n){
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

