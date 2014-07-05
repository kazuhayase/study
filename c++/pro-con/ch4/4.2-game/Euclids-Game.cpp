#include <cstdio>
#include <algorithm>
using namespace std;
//INPUT
int a,b;

void solve(){
  bool f = true;
  for(;;){
    if (a > b) swap (a,b);

    // b is a's multiple
    if (b % a == 0) break;

    // the case 2 ( free to choose a(x-1) or ax)
    if (b - a > a) break;

    b -= a;
    f = !f;
  }
  if (f) puts ("Stan wins");
  else puts ("Ollie wins");
}

int main(){
  a=34, b=12;
  solve();

  a=15, b=24;
  solve();
}
