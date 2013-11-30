#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 1000;

int n,m,k[MAX_N];
bool answer;

void read();
void solve();
void write();

int main(){
  read();
  solve();
  write();
  return 0;
}

void solve(){

  answer = false;
  
}
    
void read (){
  scanf("%d %d", &n, &m);
  for (int i = 0; i < n; i++){
    scanf("%d", &k[i]);
  }
}

void write (){
  if (answer) puts("Yes");
  else puts("No");
}
