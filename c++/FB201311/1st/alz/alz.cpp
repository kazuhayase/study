#include <cstdio>
#include <iostream>
#include <algorithm>
#include <vector>
#include <map>
#include <set>

using namespace std;

const int INF = 1000000;

int T;
const int MAX_T = 20;

int N,K;
const int MAX_N = 20;

int A[MAX_N];
int AK[MAX_N];
int WK[MAX_N];
const int MAX_A = 50;
const int MAX_P = 100;

bool is_prime[MAX_P+1];

int primeValue[MAX_P+1];// constant
//#i of WK[i] which is factored to it. 
int primeCount[MAX_P+1];// need to be initialized

vector<int> fact[MAX_P+1];// constant
//#i of WK[i] which has common primes (multiple counted)
int factCount[MAX_P+1];// need to be initialized
//set of WK[i] which has common primes (multiple counted)
set<int> factSet[MAX_P+1];// need to be initialized

// need to be initialized
int ageValue[MAX_N];
int ageDist[MAX_N];
int ageNext[MAX_N];

void init(int n){

  //sieve
  for(int i=0; i<=n; i++) is_prime[i]=true;
  is_prime[0]=is_prime[1]=false;

  int p=2; 
  for(int i=2; i<=n; i++){
    if(is_prime[i]){
      primeValue[p++] = i;
      for(int j=2*i; j<=n; j+=i) is_prime[j]=false;
    }
  }

  //prime factors
  for(int i=2; i<=n; i++){
    int j=2;
    int k=i;
    while(primeValue[j]<=k && primeValue[j]>0){
      if(k % primeValue[j] == 0){
	fact[i].push_back(j);
	while(k % primeValue[j] == 0){
	  k /= primeValue[j];
	}
      }
      j++;
    }
  }
}

void init_work(int n){

  //init working spaces
  //primeCount -> 0
  //factCount -> 0
  //factSet -> empty
  //ageValue->0,ageDist->INF,ageNext->INF

  for(int i=0; i<=n; i++){
    primeCount[i]=0;
    factCount[i]=0;
    factSet[i].clear();
  }

  for(int i=0; i<=n; i++){
    ageValue[i]=0;
    ageDist[i]=INF;
    ageNext[i]=INF;
  }

}


void read_T();
void read();
void solve(int t);

int main(){
  read_T();
  init(MAX_P);
  for(int t=0; t < T; t++){
    read();
    init_work(MAX_P);
    solve(t);
  }
  return 0;
}

void read_T(){
  cin >> T;
  fprintf(stderr, "T=%d\n", T);
}

void read(){
  scanf("%d %d\n", &N, &K);
  fprintf(stderr, "N=%d, K=%d\n", N,K);
  for(int i=0; i<N; i++){
    scanf("%d", &A[i]);
  }
}

void alignK(){
  if(K==1){
    for(int i=0; i<N; i++){
      AK[i]=A[i];
      WK[i]=AK[i];
    }
    return;
  } else {
    for(int i=0; i<N; i++){
      if(A[i] % K !=0){
	AK[i] = (A[i]/K + 1) * K;
      } else {
	AK[i] = A[i];
      }
      WK[i]=AK[i]/K;
    }
    return;
  }
}


void solve(int t){

  alignK();
  
  // count #WK[i] in prime/fact
  int count1=0;
  for(int i=0; i<N; i++){
    if(WK[i]==0) continue;
    if(WK[i]==1) {
      if(count1==0) {
	count1++;
	continue;
      }
      else WK[i]=2;
    }
    vector<int>::iterator fit = fact[WK[i]].begin();
    while(fit != fact[WK[i]].end()){
      primeCount[*fit]++;
      int p=primeValue[*fit];
      for(int j=p; j <= MAX_P; j += p){
	factCount[j]++;
	factSet[j].insert(i);
      }
      fit++;
    }
  }
  
  while(true){  
    // find next & calc dist
    int min_dist=INF;
    int min_idx=INF;
    for(int i=0; i<N; i++){
      if(WK[i]==0||WK[i]==1) {
	ageDist[i]=INF;
	continue;
      }
      int j=WK[i];
      //if(factCount[j]==1){
      if(factSet[j].size()==1){
	ageDist[i]=INF;
	continue;
      }
      while(j<MAX_P+1){
	j++;
	//if(factCount[j]==0){
	if(factSet[j].size()==0){
	  ageDist[i]=j-WK[i];
	  //next[i]=j;
	  if(min_dist>ageDist[i]){
	    min_dist = ageDist[i];
	    min_idx=i;
	  }
	}

	// 14=>16 (WK[i]=14, j=16)
	//if(factCount[j]==1){
	if(factSet[j].size()==1 && factSet[j].find(i)!=factSet[j].end()){
	  ageDist[i]=j-WK[i];
	  if(min_dist>ageDist[i]){
	    min_dist = ageDist[i];
	    min_idx=i;
	  }
	}
	/*
	  bool mflg = false;
	  vector<int>::iterator wit = fact[WK[i]].begin();
	  while(wit != fact[WK[i]].end()){
	    int p=primeValue[*wit];
	    if(j % p == 0) mflg=true;
	    wit++;
	  }
	  if(mflg){
	    ageDist[i]=j-WK[i];
	    //next[i]=j;
	    if(min_dist>ageDist[i]){
	      min_dist = ageDist[i];
	      min_idx=i;
	      }
	    }
	  }
	*/
      }
      if(j==MAX_P+1){
	//next[i]=INF;
	ageDist[i]=INF;
      }
    }
    
    // all fact count of WK is 1.
    if(min_dist == INF){
      //fprintf("ERROR; we can't find next position\n");
      //exit(1);
      
      int diff=0;
      for(int i=0; i<N; i++){
	fprintf(stderr, "WK[%d]=%d\n", i, WK[i]);
	diff += K * WK[i] - A[i];
      }
      
      printf("Case #%d: %d\n", t+1, diff);
      return;
    } else {
      
      // move min WK to next
      
      vector<int>::iterator fit = fact[WK[min_idx]].begin();
      while(fit != fact[WK[min_idx]].end()){
	primeCount[*fit]--;
	int p=primeValue[*fit];
	for(int j=p; j <= MAX_P; j += p){
	  set<int>::iterator sit = factSet[j].find(min_idx);
	  if(sit != factSet[j].end()){
	    factSet[j].erase(sit++);
	  }
	  factCount[j]--;
	}
	fit++;
      }
      
      WK[min_idx] += min_dist;
      
      fit = fact[WK[min_idx]].begin();
      while(fit != fact[WK[min_idx]].end()){
	primeCount[*fit]++;
	int p=primeValue[*fit];
	for(int j=p; j <= MAX_P; j += p){
	  factSet[j].insert(min_idx);
	  factCount[j]++;
	}
	fit++;
      }
    }
  }
}

