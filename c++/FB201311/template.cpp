#include <cstdio>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>

using namespace std;

int T;
const int MAX_T = 20;

int n[MAX_T];
const int MAX_N = 1000;

char s[MAX_T][MAX_N][MAX_N];

void read_T();
void read();
void solve(int t);

int main(){
  read_T();
  for(int t=0; t < T; t++){
    read();
    solve(t);
  }
  return 0;
}

void read_T(){
  cin >> T;
  fprintf(stderr, "T=%d\n", T);
}

void read(){
  scanf("%d", &n);
  fprintf(stderr, "n; %d\n", n);
}

void solve(int t){

  int ans;
  printf("Case #%d: %s\n", t+1, (ans == 1) ? "YES" : "NO");

}
