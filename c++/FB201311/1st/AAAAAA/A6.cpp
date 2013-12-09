#include <cstdio>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>

using namespace std;

int T;
const int MAX_T = 20;

int N,M;
const int MAX_N = 500;

char field[MAX_N][MAX_N+1];

void read_T();
void read();
void solve(int t);

int main(){
  read_T();
  for(int t=0; t < T; t++){
    read();
    solve(t);
  }
  return 0;
}

void read_T(){
  cin >> T;
  fprintf(stderr, "T=%d\n", T);
}

void read(){
  scanf("%d %d\n", &N, &M);
  fprintf(stderr, "N=%d, M=%d\n", N,M);
  fill(field,field+N*(M+1),'\0');

  for(int i=0; i<N; i++){
    for(int j=0; j<M; j++){
      scanf("%c", &field[i][j]);
    }
    scanf("\n");
    //fprintf(stderr, "field[%d] = '%s'\n", i, field[i]);
  }
  //scanf("\n");
}

// status = (x,y,rev,
// dir; 0=right or down, 1=left, 2=up
// reved; false=none, true=once
// return maximal length

int dx[2]={1,0};
int dy[2]={0,1};

int rdx[2]={-1,0};
int rdy[2]={0,-1};

int dfs(int x, int y, int dir, bool reved){

  int length=0;
  
  field[y][x]='t';

  // down or right
  for(int i=0; i<2; i++){
    int nx = x + dx[i], ny = y + dy[i];
    if(0 <= nx && nx < M && 0 <= ny && ny < N && field[ny][nx] == '.'){
      length = max (length, dfs(nx, ny, 0, reved)+1);
    }
  }

  // up or left
  for(int i=0; i<2; i++){
    int nx = x + rdx[i], ny = y + rdy[i];
    if(0 <= nx && nx < M && 0 <= ny && ny < N && field[ny][nx] == '.' 
       && (dir == i+1 || (dir == 0 && reved ==false)) ){
      length = max (length, dfs(nx, ny, i+1, true)+1);
    }
  }
  field[y][x] = '.';
  return length;
}

void solve(int t){
  int ans = dfs(0,0,0,false)+1;
  printf("Case #%d: %d\n", t+1, ans);

}
