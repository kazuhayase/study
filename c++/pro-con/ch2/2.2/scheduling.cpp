#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 100000;

int N, S[MAX_N], T[MAX_N];

pair<int,int> itv[MAX_N];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d", &N);
  for (int i=0; i<N; i++){
    scanf("%d", &S[i]);
  }
  for (int i=0; i<N; i++){
    scanf("%d", &T[i]);
  }

}

void solve(){

  for (int i=0; i<N; i++){
    itv[i].first = T[i];
    itv[i].second = S[i];
  }

  sort(itv, itv+N);

  int ans=0, t=0;

  for (int i=0; i<N; i++){
    if (t < itv[i].second){
      ans++;
      t = itv[i].first;
    }
  }

  printf("%d\n", ans);

}
