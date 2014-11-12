#include "MaxFlow-Dinic-for-TheYearOfCodeJam.cpp"
const int dx[4]={-1,0,0,1}, dy[4]={0,-1,1,0};
const int MAX_N=50;
const int MAX_M=50;

//INPUT
int N, M;
char cld[MAX_N][MAX_M+1];//calendar

void solve(){
  int res=0;
  int s = N*M, t = s+1;
  for(int i=0; i<N; i++){
    for(int j=0; j<M; j++){
      if ((i+j) % 2 == 0){
	if (cld[i][j] == '#'){
	  res +=4;
	  add_edge(s, i*M+j, INF);
	} else if (cld[i][j] == '.'){
	  add_edge(i*M+j, t, INF);
	} else {
	  res += 4;
	  add_edge(s, i*M+j, 4);
	}
	for (int k=0; k<4; k++){
	  int i2 = i + dx[k], j2 = j+dy[k];
	  if (0 <= i2 && i2 < N && 0 <= j2 && j2 < M){
	    add_edge(i*M+j, i2*M+j2, 2);
	  }
	}
      } else {
	if (cld[i][j] == '#'){
	  res +=4;
	  add_edge(i*M+j, t, INF);
	} else if (cld[i][j] == '.'){
	  add_edge(s, i*M+j, INF);
	} else {
	  res += 4;
	  add_edge(i*M+j, t, 4);
	}
      }
    }
  }
  res -= max_flow(s, t);
  printf("%d\n", res);
}

int main(){
  N=3, M=3;
  cld[0][0]='.', cld[0][1]='?', cld[0][2]='.';
  cld[1][0]='.', cld[1][1]='?', cld[1][2]='.';
  cld[2][0]='.', cld[2][1]='#', cld[2][2]='.';
  solve();

  for(int i=0; i<MAX_V; i++){
    G[i].clear();
  }

  N=5, M=8;
  cld[0][0]='.', cld[0][1]='#', cld[0][2]='.', cld[0][3]='.',
    cld[0][4]='.', cld[0][5]='#', cld[0][6]='#', cld[0][7]='.';

  cld[1][0]='.', cld[1][1]='#', cld[1][2]='#', cld[1][3]='.',
    cld[1][4]='.', cld[1][5]='?', cld[1][6]='.', cld[1][7]='.';

  cld[2][0]='.', cld[2][1]='#', cld[2][2]='#', cld[2][3]='#',
    cld[2][4]='.', cld[2][5]='#', cld[2][6]='.', cld[2][7]='#';

  cld[3][0]='?', cld[3][1]='?', cld[3][2]='#', cld[3][3]='.',
    cld[3][4]='.', cld[3][5]='?', cld[3][6]='.', cld[3][7]='.';

  cld[4][0]='#', cld[4][1]='#', cld[4][2]='#', cld[4][3]='?',
    cld[4][4]='#', cld[4][5]='.', cld[4][6]='.', cld[4][7]='.';

  solve();
}
