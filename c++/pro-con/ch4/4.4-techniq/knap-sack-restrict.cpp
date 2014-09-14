#include<cstdio>
#include <algorithm>
using namespace std;

//using sliding minimum (using deq) technique

//INPUT
const int MAX_N = 10000;
const int MAX_W = 10000;
int n, W;
int w[MAX_N], v[MAX_N], m[MAX_N];

int dp[MAX_W + 1]; // DP table

int deq[MAX_W + 1]; // deq for index
int deqv[MAX_W + 1]; // deq for value

void solve(){
  for (int i=0; i<n; i++){
    for (int a=0; a < w[i]; a++){
      int s=0, t=0; // deq head & tail
      for (int j=0; j * w[i] + a <= W; j++) {
	// add j to tail of deq
	int val = dp [j * w[i] + a] - j * v[i];
	while (s < t && deqv[t-1] <= val) t--;
	deq[t] = j;
	deqv[t++] = val;
	// take out the head of the deq
	dp[j * w[i] + a] = deqv[s] + j * v[i];
	if (deq[s] == j - m[i]) {
	  s++;
	}
      }
    }
  }
  printf("%d\n", dp[W]);
}

int main(){
  n=3, W=12;
  w[0] = 3, v[0] = 2, m[0] = 5;
  w[1] = 2, v[1] = 4, m[1] = 1;
  w[2] = 4, v[2] = 3, m[2] = 3;
  solve();
}
