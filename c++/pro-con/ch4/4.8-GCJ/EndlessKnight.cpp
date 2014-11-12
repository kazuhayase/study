#include<cstdio>
#include<algorithm>
#include "ModComb-for-EndlessKnight.cpp"

using namespace std;
const int MOD = 10007;
const int MAX_R = 10;

typedef pair<int, int> P;

// normarize to move horizontal and vertical
// return false if unreachable
bool normarize(int& x, int& y){
  --x; --y;
  int xx = -x + 2 * y, yy = 2 * x -y;
  if (xx < 0 || yy < 0 || xx % 3 != 0 || yy % 3 != 0) return false;
  x = xx / 3; y = yy / 3;
  return true;
}

int count_bit(int a){
  int res=0;
  for(; a>0; a >>= 1) res += a & 1;
  return res;
}

//INPUT
int H, W, R;
P ps[MAX_R + 1];

void solve(){
  pre_compute_mod_fact(MOD);

  int pn=0;
  for(int i=0; i<R; i++){
    if(normarize(ps[i].first, ps[i].second)) {
      ps[pn++] = ps[i];
    }
  }

  //if the goal is unreachable, res=0
  ps[pn] = P(H, W);
  if (!normarize(ps[pn].first, ps[pn].second)){
    printf("0\n");
    return;
  }
  int res=0;
  sort(ps, ps+pn);
  
  for (int i=0; i<1 << pn; i++){
    int add=1, prevx=0, prevy=0;
    for (int j=0; j < pn+1; j++){
      if( (i >> j) % 2 == 1 || j == pn){
	int mx = ps[j].first - prevx, my = ps[j].second - prevy;
	add = add * mod_comb(mx + my, mx, MOD) % MOD;
	prevx = ps[j].first;
	prevy = ps[j].second;
      }
    }
    if (count_bit(i) % 2 == 0){
      res = (res + add) % MOD;
    } else {
      res = (res - add + MOD) % MOD;
    }
  }
  printf("%d\n", res);
}

int main(){
  H=4, W=4, R=1;
  ps[0] = P(2,1);
  solve();

  H=3, W=3, R=0;
  solve();

  H=7, W=10, R=2;
  ps[0] = P(1,2);
  ps[1] = P(7,1);
  solve();


}
