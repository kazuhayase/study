#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 1000;

int N,R;
int X[MAX_N];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d\n", &N);
  scanf("%d\n", &R);

  for(int i=0; i<N; i++){
    scanf("%d", &X[i]);
  }
}

void solve(){

  sort(X, X+N);

  int i=0, ans=0;

  while(i<N){
    int s = X[i++];
    while (i<N && X[i] <= s+R) i++;

    int p = X[i-1];
    while (i<N && X[i] <= p+R) i++;

    ans++;
  }

  printf("%d\n", ans);

}
