// pre computation on t[i] & s[j] (next[i])
// binary search by next[k][i]
// O(N log N) 

#include<cstdio>
#include <algorithm>
using namespace std;

//INPUT
const int MAX_N = 10000;
const int MAX_LOG_N = 15;
int N,M;
int s[MAX_N*2], t[MAX_N*2];

pair<int, int> ps[MAX_N * 4];
int next[MAX_LOG_N][MAX_N * 2];

void solve(){
  int res = 0;

  // two cycles
  for (int i=0; i < N; i++){
    if (t[i] < s[i]) t[i] += M;
    s[N+i] = s[i] + M;
    t[N+i] = t[i] + M;
  }

  // sort by end time
  for (int i=0; i < N*2; i++){
    ps[i] = make_pair(t[i], i);
    ps[N*2 + i] = make_pair(s[i], N*2 + i);
  }
  sort(ps, ps+N*4);

  // precomputation of next[0]
  int last=-1;
  for(int i = N * 4 -1; i >= 0; i--){
    int id = ps[i].second;
    if(id < N*2){
      // end of a segment
      next[0][id]=last;
    } else {
      // head of a segment
      id -= N*2;
      if (last < 0 || t[last] > t[id]) {
	last = id;
      }
    }
  }

  // computation of next
  for(int k=0; k+1 < MAX_LOG_N; k++){
    for(int i=0; i < N*2; i++){
      if(next[k][i] < 0) next[k+1][i] = -1;
      else next[k+1][i] = next[k][next[k][i]];
    }
  }
  
  // fix the first segment
  for(int i=0; i<N; i++){
    // greedy
    int tmp=0, j=i;
    for(int k=MAX_LOG_N - 1; k >=0; k--){
      int j2 = next[k][j];
      if (j2 >= 0 && t[j2] <= s[i] + M){
	j = j2;
	tmp |= 1 << k;
      }
    }
    res = max(res, tmp+1);
  }
  printf("%d\n", res);
}

int main(){
  N=3, M=10;
  s[0]=0, t[0]=3;
  s[1]=3, t[1]=7;
  s[2]=7, t[2]=0;
  solve();

  N=3, M=10;
  s[0]=0, t[0]=5;
  s[1]=2, t[1]=7;
  s[2]=6, t[2]=9;
  solve();
}

