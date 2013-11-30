#include <cstdio>

int t;
const int MAX_T = 20;

int n[MAX_T];
const int MAX_N = 20;

char s[MAX_T][MAX_N][MAX_N];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d\n", &t);
  fprintf(stderr, "t; %d\n", t);

  for(int i=0; i < t; i++){
    scanf("%d", &n[i]);
    fprintf(stderr, "n[%d]; %d\n", i, n[i]);
    for(int j=0; j < n[i]; j++){
      gets(s[i][j]);
      fprintf(stderr, "s[%d][%d]%s\n", i,j,s[i][j]);
  }

}

void solve(){

  int i;
  int ans;

  for (i = 0; i < t; i++){
    printf("Case #%d: %s\n", i+1, (ans == 1) ? "YES" : "NO");
  }
}
