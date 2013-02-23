// example for DFS
#include <cstdio>
#include <algorithm>

using namespace std;

const int MAX_N = 100;

int N,M;
char field[MAX_N][MAX_N + 1];

int answer;

void read();
void solve();
void write();

int main(){
  read();
  solve();
  write();
  return 0;
}

void dfs(int x, int y){
  // replace current position to .
  field[x][y] = '.';

  // 8 directions
  for (int dx = -1; dx <= 1; dx++){
    for (int dy = -1; dy <= 1; dy++){
      int nx = x + dx, ny = y + dy;
      if (0 <= nx && nx < N && 0 <= ny && ny < M && field[nx][ny] == 'W') dfs(nx, ny);
    }
  }
  return;
}
      

void solve(){

  answer = 0;
  for (int i=0; i<N; i++){
    for (int j=0; j<M; j++){
      if (field[i][j] == 'W'){
	dfs(i,j);
	answer++;
      }
    }
  }
}
    
void read (){
  scanf("%d", &N);
  scanf("%d\n", &M);
  for (int i = 0; i < N; i++){
    scanf("%s", field[i]);
  }
}

void write (){
  printf("%d\n", answer);
}
