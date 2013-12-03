#include <cstdio>
#include <algorithm>
#include <queue>

using namespace std;

const int MAX_N = 20000;

typedef long long ll;

int N;
int L[MAX_N];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d\n", &N);

  for(int i=0; i<N; i++){
    scanf("%d", &L[i]);
  }
}

void solve(){

  ll ans=0;

  priority_queue<int, vector<int>, greater<int> > que;
  for(int i=0; i<N; i++){
    que.push(L[i]);
  }

  while(que.size() > 1){
    int l1,l2;
    l1 = que.top();
    que.pop();
    l2 = que.top();
    que.pop();

    ans += l1+ l2;
    que.push(l1+l2);

  }

  printf("%lld\n", ans);

}
