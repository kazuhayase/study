#include<cstdio>
#include<algorithm>
using namespace std;

const int MAX_N = 100000;
int n,S;
int a[MAX_N];

int sum[MAX_N + 1];

void solve(){
  for(int i=0; i<n; i++){
    sum[i+1] = sum[i] + a[i];
  }
  if (sum[n]<S){
    printf("0\n");
    return;
  }

  int res=n;
  for(int s=0; sum[s]+S<=sum[n]; s++){
    int t = lower_bound(sum+s, sum+n, sum[s]+S) -sum;
    res = min(res, t-s);
  }

  printf("%d\n", res);
}
