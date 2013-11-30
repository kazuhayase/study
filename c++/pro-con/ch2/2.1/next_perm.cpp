const int MAX_N = 100;

bool used[MAX_N];
int perm[MAX_N];



void permutation1 (int pos, int n) {
  if (pos == n) {
    // do something on perm[]
    return;
  }

  for (int i=0; i<n; i++){
    if (!used[i]){
      perm[pos] = i;
      used[i]=true;
      permutation1(pos+1, n);
      used[i]=false;
    }
  }
  return;
}

#include <algorithm>

int perm2[MAX_N];

using namespace std;

void permutation2(int n) {
  for (int i = 0; i<n; i++){
    perm2[i] = i;
  }

  do {
    // do something on perm2[]
  } while (next_permutation(perm2, perm2+n));
  return;
}

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){}
void solve(){}
