#include <cstdio>
#include <algorithm>
<<<<<<< HEAD

using namespace std;

const int MAX_N = 100;
const int MAX_A = 1000000;

int n, a[MAX_N];
int ans;

void read();
void solve();
void write();
=======
using namespace std;

const int MAX_N = 50;

int n, a[MAX_N];

void read();
void solve();
>>>>>>> 6d842800eb378862be82e623b679a20d6472a172

int main(){

  read();
  solve();
<<<<<<< HEAD
  write();
  return 0;

}

void solve() {
  ans = 0;

  for(int i=0; i<n; i++){
    for(int j=i+1; j<n; j++){
      for(int k=j+1; k<n; k++){
	int len = a[i]+a[j]+a[k];
	int ma = max(a[i], max(a[j],a[k]));
	int rest = len - ma;
	if(ma < rest){
	  ans = max (ans, len);
	}}}}
}

=======
  return 0;

}
void solve(){

  int ans=0;

  for (int i=0; i < n; i++){
    for (int j=i+1; j < n; j++){
      for (int k=j+1; k < n; k++){
	int len = a[i] + a[j] + a[k];
	int ma = max(a[i], max(a[j], a[k]));
	int rest = len - ma;

	if (ma < rest){
	  ans = max (ans, len);
	}
      }
    }
  }

  printf ("%d\n", ans);
}


>>>>>>> 6d842800eb378862be82e623b679a20d6472a172
void read (){
  scanf("%d", &n);
  for (int i = 0; i < n; i++){
    scanf("%d", &a[i]);
  }
}
<<<<<<< HEAD

void write (){
  printf("%d\n", ans);
}
=======
>>>>>>> 6d842800eb378862be82e623b679a20d6472a172
