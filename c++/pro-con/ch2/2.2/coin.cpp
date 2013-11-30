#include <cstdio>
#include <algorithm>

using namespace std;

int C[6], A;
int V[6] = {1,5,10,50,100,500};

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  for(int i=0; i < 6; i++){
    scanf("%d", &C[i]);
  }
  scanf("%d", &A);
}

void solve(){

  int ans=0;

  for (int i=5; i>=0; i--){
    int t = min (A / V[i], C[i]);
    A -= t*V[i];
    ans += t;
  }

  printf("%d\n", ans);

}
