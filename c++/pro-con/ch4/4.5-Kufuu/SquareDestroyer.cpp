#include<cstdio>
#include<vector>
#include <algorithm>
using namespace std;

const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

//INPUT (processed numbers)
const int MAX_MATCH=100;
const int MAX_SQUARE=100;

// M = # of matches, S = # of squares
int M,S;
// m[i][j] == true <-> match i is included in square j
bool m[MAX_MATCH][MAX_SQUARE];
// mmax[i] = max destroyer of square i
int mmax[MAX_SQUARE];

// minimal resolution
int min_res;

// lower bound by considering after p
int hstar(int p, vector<bool> state){
  vector <pair <int, int> > ps;
  for (int i=0; i<S; i++){
    if (state[i]){
      // count matches in the exisiting squares
      int num = 0; 
      for (int j=p; j<M; j++){
	if(m[j][i]) num++;
      }
      ps.push_back(make_pair(num, i));
    }
  }
  // sort ascending on #matches
  sort(ps.begin(), ps.end());
  int res = 0;

  // used[i] == true <-> X includes a square which includes match i
  vector<bool> used(M, false);
  for(int i=0; i<ps.size(); i++){
    int id = ps[i].second;
    bool ok = true;
    // check if square id can be added to X
    for (int j=p; j<M; j++){
      if (used[j] && m[j][id]) ok = false;
    }
    if (ok) {
      res++;
      for (int j=p; j < M; j++){
	if (m[j][id]) used[j]=true;
      }
    }
  }
  return res;
}

// p is match id, num is # of removed matches
// state[i] == true <-> square i is alive
int dfs(int p, int num, vector<bool> state){
  // if all matches are processed, all square are destroyed
  if (p == M) return min_res = num;

  //if(num >= min_res) return INF;
  if(num + hstar(p, state) >= min_res) return INF;

  // match p must be removed; use == true
  // match p must not be removed; notuse == true
  bool use = false, notuse = true;
  for (int i = 0; i < S; i++){
    // As match p can destroy square i, p can be removed
    if (state[i] && m[p][i]) notuse = false;

    // As match p must destroy square i, p must be removed
    if (state[i] && mmax[i]==p) use = true;
  }

  int res = INF;
  // case of p is not removed
  if (!use) res = min(res, dfs(p+1, num, state));

  // case of p is removed
  for (int i=0; i<S; i++){
    if (m[p][i]) state[i]=false;
  }
  if (!notuse) res = min(res, dfs(p+1, num+1, state));
  return res;
}

void solve(){
  vector<bool> state(S, true);
  printf("%d\n", dfs(0,0,state));
}

// IDA* 
// x -> 0,1,....
// check if there is a solution with value less than or equal to x

void solve_ida(){
  vector<bool> state(S, true);

  //min_res -> 0,1,...
  while(dfs(0,0,state) == INF) min_res++;
  printf("%d\n", min_res);
}


/*
int main(){
  M = 12, S = 4;
  m[0][0]=true, ...
*/
