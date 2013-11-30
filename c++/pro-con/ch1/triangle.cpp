#include <cstdio>
#include <algorithm>
using namespace std;

const int MAX_N = 50;

int n, a[MAX_N];

void read();
void solve();

int main(){

  read();
  solve();
  return 0;

}
void solve(){

  int ans=0;

  for (int i=0; i < n; i++){
    for (int j=i+1; j < n; j++){
      for (int k=j+1; k < n; k++){
	int len = a[i] + a[j] + a[k];
	int ma = max(a[i], max(a[j], a[k]));
	int rest = len - ma;

	if (ma < rest){
	  ans = max (ans, len);
	}
      }
    }
  }

  printf ("%d\n", ans);
}


void read (){
  scanf("%d", &n);
  for (int i = 0; i < n; i++){
    scanf("%d", &a[i]);
  }
}
