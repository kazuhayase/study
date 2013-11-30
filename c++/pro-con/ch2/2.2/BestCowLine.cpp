#include <cstdio>

const int MAX_N = 2000;
int N;
char S[MAX_N+1];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d\n", &N);
  for (int i=0; i<N; i++){
    scanf("%c", &S[i]);
  }
}

void solve(){
  int a=0, b=N-1;

  while(a<=b){
    bool left = false;
    for (int i=0; a+i <= b; i++){
      if (S[a+i] < S[b-i]){
	left = true;
	break;
      }
      else if (S[a+i] > S[b-i]){
	left = false;
	break;
      }
    }

    if (left) putchar (S[a++]);
    else putchar (S[b--]);
  }
  putchar ('\n');
}
