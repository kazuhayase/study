#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 1000000;;

int l, n, x[MAX_N];
int minT, maxT;

void read();
void solve();
void write();

int main(){

  read();
  solve();
  write();
  return 0;

}

void solve() {
  minT = 0, maxT=0;

  for(int i=0; i<n; i++){
    minT = max(minT, min(x[i], l-x[i]));
  }

  for(int i=0; i<n; i++){
    maxT = max(maxT, max(x[i], l-x[i]));
  }

}

void read (){
  scanf("%d", &l);
  scanf("%d", &n);
  for (int i = 0; i < n; i++){
    scanf("%d", &x[i]);
  }
}

void write (){
  printf("%d %d\n", minT, maxT);
}
