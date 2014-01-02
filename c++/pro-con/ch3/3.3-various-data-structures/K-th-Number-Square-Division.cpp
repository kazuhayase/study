#include <cstdio>
#include <climits>
#include <cmath>
#include <iostream>
#include <algorithm>
#include <map>
#include <set>
#include <vector>

using namespace std;

const int MAX_N = 100000;
const int MAX_M = 5000;
const int INF = std::numeric_limits<int>::max(); //2,147,483,647 == 2^31 -1

const int B=1000; //bucket size

//INPUT

int N,M;
int A[MAX_N];
int I[MAX_N], J[MAX_N], K[MAX_N];
int nums[MAX_N];
vector<int> bucket[MAX_N / B];

void solve(){
  for(int i=0; i<N; i++){
    bucket[i / B].push_back(A[i]);
    nums[i] = A[i];
  }
  sort(nums, nums+N);

  for(int i=0; i<N/B; i++) sort(bucket[i].begin(), bucket[i].end());

  for(int i=0; i<M; i++){
    int l=I[i], r=J[i]+1, k=K[i];
    int lb=-1, ub=N-1;
    while(ub - lb > 1){
      int md = (lb+ub)/2;
      int x = nums[md];
      int tl = l, tr = r, c = 0;

      // Hamidashi
      while(tl < tr && tl % B != 0) if (A[tl++] <= x) c++;
      while(tl < tr && tr % B != 0) if (A[--tr] <= x) c++;

      //for each bucket
      while(tl < tr){
	int b = tl / B;
	c += upper_bound(bucket[b].begin(), bucket[b].end(), x) - bucket[b].begin();
	tl += B;
      }
      if (c >= k) ub = md;
      else lb = md;
    }
    printf("%d\n", nums[ub]);
  }
}

int main(){
  solve();
  return 0;
}

