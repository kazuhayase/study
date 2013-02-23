// example for BFS
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <queue>

using namespace std;

const int INF = 100000000;
const int MAX_N = 100;
const int MAX_M = 100;

typedef pair<int, int> P;

int N,M;
int sx,sy;
int gx,gy;
char maze[MAX_N][MAX_M];
int d[MAX_N][MAX_M];

int dx[4] = {1, 0, -1, 0}, dy[4]={0, 1, 0, -1};

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

int bfs() {
  queue<P> que;

  for (int i=0; i<N; i++){
    for (int j=0; j<M; j++){
      d[i][j] = INF;
    }
  }

  que.push(P(sx,sy));
  d[sx][sy]=0;


  while (que.size()){
    P p = que.front(); que.pop();

    if (p.first == gx && p.second == gy) {
      break;
    }

    for (int i=0; i<4; i++){
      int nx = p.first + dx[i], ny = p.second + dy[i];

      if (0 <= nx && nx < N && 0 <= ny && ny < M && maze[nx][ny] != '#' && d[nx][ny] == INF) {
	que.push(P(nx, ny));
	d[nx][ny] = d[p.first][p.second] + 1;
      }
    }
  }
  return d[gx][gy];
}

void solve(){
  answer = bfs();
}
    
void read (){
  scanf("%d", &N);
  scanf("%d\n", &M);
  for (int i = 0; i < N; i++){
    for (int j = 0; j < M; j++){
      scanf("%c", &maze[j][i]);

      switch (maze[j][i]){
	
      case 'S':
	sx = j, sy =i;
	break;
      case 'G':
	gx = j, gy =i;
	break;
      default: 
	break;
      }
    }
    scanf("%*c");
  }
}

void write (){
  printf("%d\n", answer);
}
