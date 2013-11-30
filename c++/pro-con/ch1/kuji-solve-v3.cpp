#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 50;

int n,m,k[MAX_N],kk[MAX_N * MAX_N];

void read();
void solve();

int main(){

  read();
  solve();
  return 0;

}

bool binary_search(int x) {
  int l = 0, r = n * n;
  while (r - l >= 1) {
    int i = (l+r) / 2;
    if (kk[i] == x) return true;
    else if (kk[i] < x) l=i+1;
    else r = i;
  }
  return false;
}

void solve(){
  for (int c = 0; c < n; c++){
    for (int d = 0; d < n; d++){
      kk[c * n + d] = k[c] + k[d];
    }
  }

  sort(kk, kk+n*n);

  // flag (answer)
  bool f = false;

  // quad loop
  for (int a = 0; a < n; a++){
    for (int b = 0; b < n; b++){
      if (binary_search(m - k[a] - k[b])){
	f = true;
      }
    }
  }
  
  
  // write to standard output
  if (f) puts("Yes");
  else puts("No");
  
}


    
  // read from standard input
void read (){
  scanf("%d %d", &n, &m);
  for (int i = 0; i < n; i++){
    scanf("%d", &k[i]);
  }
}
