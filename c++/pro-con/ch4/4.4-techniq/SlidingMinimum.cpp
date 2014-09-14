#include<cstdio>
#include <algorithm>
using namespace std;

// Using "Deque" O(n) 
//  x[i]<x[i+1] && a[x[i]] < a[x[i+1]]
//   (cf) in case of "RMQ", O(n log(n))

//INPUT
const int MAX_N = 100000;
int n, k;
int a[MAX_N];

int b[MAX_N];
int deq[MAX_N];

void solve(){
  int s=0, t=0; // head / tail of the deq

  for (int i=0; i < n; i++){
    // add i to the deq
    while (s<t && a[deq[t-1]] >= a[i]) t--;
    deq[t++] = i;

    if (i - k + 1 >= 0){
      b[i - k + 1] = a[deq[s]];

      if (deq[s] == i - k + 1){
	// take the head of the deq
	s++;
      }
    }
  }

  for (int i = 0; i <= n-k; i++) {
    printf("%d%c", b[i], i == n-k ? '\n' : ' ');
  }
}

int main (){
  n=5, k=3;
  a[0]=1, a[1]=3, a[2]=5, a[3]=4, a[4]=2;
  solve();
}
