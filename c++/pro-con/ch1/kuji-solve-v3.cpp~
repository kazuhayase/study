#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 50;

int n,m,k[MAX_N];

void read();
void solve();

int main(){

  read();
  solve();
  return 0;

}

bool binary_search(int x) {
  int l = 0, r = n;
  while (r - l >= 1) {
    int i = (l+r) / 2;
    if (k[i] == x) return true;
    else if (k[i] < x) l=i+1;
    else r = i;
  }
  return false;
}

void solve(){

  sort(k, k+n);

  // flag (answer)
  bool f = false;

  // quad loop
  for (int a = 0; a < n; a++){
    for (int b = 0; b < n; b++){
      for (int c = 0; c < n; c++){
	if (binary_search(m - k[a] - k[b] - k[c])){
	    f = true;
	  }
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
