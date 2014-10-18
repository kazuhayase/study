#include <cstdio>
#include <set>
typedef unsigned long long ull;

using namespace std;
const int MAX_SIZE = 50;
const int MAX_T = 50;

//INPUT
int N, M, T, P, Q;
char field[MAX_SIZE][MAX_SIZE]; // search in
char patterns[MAX_T][MAX_SIZE][MAX_SIZE]; // search pattern

ull myhash[MAX_SIZE][MAX_SIZE], tmp[MAX_SIZE][MAX_SIZE];

// hash of each PxQ in a
void compute_hash(char a[MAX_SIZE][MAX_SIZE], int n, int m) {
  const ull B1 = 9973;
  const ull B2 = 100000007;

  ull t1 = 1; // B1^Q
  for (int j=0; j<Q; j++) t1 *= B1;

  // hash in row
  for (int i=0; i<n; i++){
    ull e = 0;
    for (int j=0; j<Q; j++) e = e * B1 + a[i][j];
    for (int j=0; j+Q <= m; j++){
      tmp[i][j] = e;
      if (j+Q < m) e = e * B1 - t1 * a[i][j] + a[i][j+Q];
    }
  }

  ull t2 = 1; //B2^P
  for (int i=0; i<P; i++) t2 *= B2;
  // hash in column
  for (int j=0; j+Q<=m; j++){
    ull e = 0;
    for (int i=0; i<P; i++) e = e * B2 + tmp[i][j];
    for (int i=0; i+P <= n; i++){
      myhash[i][j] = e;
      if (i+P < n) e = e * B2 - t2 * tmp[i][j] + tmp[i+P][j];
    }
  }
}

void solve(){
  //hash of patterns
  multiset<ull> unseen;
  for (int k=0; k<T; k++){
    compute_hash(patterns[k], P, Q);
    unseen.insert(myhash[0][0]);
  }

  //delete from multiset for an appearance of hash
  compute_hash(field, N, M);
  for (int i=0; i+P <=N; i++){
    for (int j=0; j+Q <=M; j++){
      unseen.erase(myhash[i][j]);
    }
  }

  int ans = T - unseen.size();
  printf("%d\n", ans);
}

int main (){
  N=M=3, P=Q=2, T=2;
  
  field[0][0]='*', field[1][0]='0', field[2][0]='0';
  field[0][1]='0', field[1][1]='*', field[2][1]='*';
  field[0][2]='*', field[1][2]='0', field[2][2]='0';

  patterns[0][0][0]='*', patterns[0][1][0]='*';
  patterns[0][0][1]='0', patterns[0][1][1]='0';

  patterns[1][0][0]='*', patterns[1][1][0]='0';
  patterns[1][0][1]='*', patterns[1][1][1]='*';

  solve();
}



