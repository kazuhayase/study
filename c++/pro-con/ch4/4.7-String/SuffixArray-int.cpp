using namespace std;

const int MAX_N = 1000;
int n,k;
int myrank[MAX_N + 1];
int tmp[MAX_N + 1];

// compare (myrank[i], myrank[i+k]) vs (myrank[j], myrank[j+k])
bool compare_sa(int i, int j){
  if(myrank[i] != myrank[j]) return myrank[i] < myrank[j];
  else {
    int ri = i+k <=n ? myrank[i+k] : -1;
    int rj = j+k <=n ? myrank[j+k] : -1;
    return ri < rj;
  }
}

void construct_sa(int *S, int *sa){
  n = (sizeof S) / (sizeof S[0]);
  // start length-1, rank is character code
  for (int i=0; i <=n; i++){
    sa[i] = i;
    myrank[i] = i < n ? S[i] : -1;
  }

  //k -> 2k
  for (k=1; k <= n; k *=2) {
    sort (sa, sa+n+1, compare_sa);
    
    // once computed in tmp and move to rank
    tmp[sa[0]] = 0;
    for (int i=1; i <= n; i++){
      tmp[sa[i]] = tmp[sa[i-1]] + (compare_sa(sa[i-1], sa[i]) ? 1 : 0);
    }
    for(int i=0; i<=n; i++){
      myrank[i] = tmp[i];
    }
  }
}

