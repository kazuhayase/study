#include<vector>
#include<cmath>

using namespace std;
const double EPS = 1E-8;
typedef vector<double> vec;
typedef vector<vec> mat;

const int MAX_N = 10;
const int MAX_M = 10;

// solve Ax = b. A is square matrix.
// if no solution or no unique solution, return an array of length=0
vec gauss_jordan(const mat& A, const vec& b){
  int n = A.size();
  mat B(n, vec(n+1));
  for(int i=0; i<n; i++)
    for(int j=0; j<n; j++) B[i][j] = A[i][j];
  // A <- Ab
  for(int i=0; i<n; i++) B[i][n] = b[i];

  for(int i=0; i<n; i++) {
    // move equation with max coefficient to the variable to i-th
    int pivot = i;
    for (int j=i; j<n; j++){
      if (abs(B[j][i]) > abs(B[pivot][i])) pivot = j;
    }
    swap(B[i], B[pivot]);

    // no solution or no unique solution
    if (abs(B[i][i]) < EPS) return vec();

    // set the cofficient to the variable to be 1
    for (int j = i+1; j <=n; j++) B[i][j] /= B[i][i];
    for (int j = 0; j <n; j++) {
      if (i != j){
	// delete the i-th variable in the j-th equation
	for (int k = i+1; k <= n; k++) B[j][k] -= B[j][i] * B[i][k];
      }
    }
  }
  vec x(n);
  // b is the solution
  for(int i=0; i<n; i++) x[i] = B[i][n];
  return x;
}


//INPUT
char grid[MAX_N][MAX_M + 1];
int N, M;

bool can_goal[MAX_N][MAX_M]; // if true, able to goal
int dx[4] = {-1,1,0,0}, dy[4] = {0,0,-1,1};

// fill can_goal
void dfs(int x, int y){
  can_goal[x][y] = true;
  for (int i=0; i<4; i++){
    int nx = x + dx[i], ny = y + dy[i];
    if (0 <= nx && nx < N && 0<= ny && ny < M 
	&& !can_goal[nx][ny] && grid[nx][ny] != '#') {
      dfs(nx, ny);
    }
  }
}

void solve(){
  mat A(N*M, vec(N*M, 0));
  vec b(N*M, 0);
  for(int x=0; x < N; x++){
    for(int y=0; y < M; y++){
      can_goal[x][y] = false;
    }
  }
  dfs(N-1, M-1);

  //build matrix
  for (int x=0; x<N; x++){
    for(int y=0; y < M; y++){
      //at goal or unable to goal
      if ( (x == N-1 && y == M-1) 
	   || !(can_goal[x][y])){
	A[x * M + y][x * M + y] = 1;
	continue;
      }

      // other than the goal
      int move = 0;
      for (int k = 0; k < 4; k++){
	int nx = x + dx[k], ny = y + dy[k];
	if (0 <= nx && nx < N && 0<= ny && ny < M 
	    && grid[nx][ny] == '.') {
	  A[x * M + y][nx * M + ny] = -1;
	  move++;
	}
      }
      b[x * M + y] = A[x * M + y][x * M + y] = move;
    }
  }
  vec res = gauss_jordan(A, b);
  printf("%.8f\n", res[0]);
}

int main(){
  N=10, M=10;

  for(int i=0; i<N; i++ ){
    for(int j=0; j<M; j++){
      grid[i][j]='.';
    }
  }
  solve();

  N=3, M=10;
  for(int i=0; i<N; i++){
    for(int j=0; j<M; j++){
      grid[i][j]='.';
    }
  }

  grid[0][1]= grid[0][5]= grid[0][9]= '#';
  grid[1][1]= grid[1][3]= grid[1][5]= grid[1][7]= grid[1][9]= '#';
  grid[2][3]= grid[2][7]= '#';

  solve();
}


