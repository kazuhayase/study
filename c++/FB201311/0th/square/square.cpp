#include <cstdio>

int t;
const int MAX_T = 20;

int n[MAX_T];
const int MAX_N = 20;

char s[MAX_T][MAX_N][MAX_N+1];

void read();
void solve();

int main(){
  read();
  solve();
  return 0;
}

void read(){
  scanf("%d\n", &t);
  fprintf(stderr, "t; %d\n", t);

  for(int i=0; i < t; i++){
    scanf("%d\n", &n[i]);
    fprintf(stderr, "n[%d]; %d\n", i, n[i]);
    for(int j=0; j < n[i]; j++){
      gets(s[i][j]);
      fprintf(stderr, "s[%d][%d]%s\n", i,j,s[i][j]);
    }
  }
}

void solve(){

  for (int i=0; i < t; i++){

    // start/end of x of the square
    int start_x=-1;
    int end_x=-1;

    // hight of the square
    int height=0;

    // flag (init = 0, in=1, out=2)
    int in_y=0;

    // answer; (init=0, yes=1, no=2)
    int ans = 0;

    for (int j=0; j < n[i]; j++){
      // flag (init = 0, in=1, out=2)
      int in_x=0;

      for (int k=0; k < n[i]; k++){
	if(s[i][j][k] == '.' && (in_x == 0 || in_x == 2) ) continue;
	if(s[i][j][k] == '.' && in_x == 1) {
	  in_x = 2;
	  if (end_x == -1){
	    end_x = k-1;

	    fprintf(stderr, "end_x is defined; j=%d, k=%d, s[%d][%d]=%s, end_x=%d\n", j,k,i,j,s[i][j],end_x);

	  } else if (end_x != k-1){
	    fprintf(stderr, "diff in end_x; j=%d, k=%d, s[%d][%d]=%s\n", j,k,i,j,s[i][j]);
	    ans = 2;
	  }
	  continue;
	}
	if(s[i][j][k] == '#' && in_x == 0) {

	  if (in_y == 2){
	    fprintf(stderr, "# after end of y; j=%d, k=%d, s[%d][%d]=%s\n", j,k,i,j,s[i][j]);
	    ans = 2;
	  }

	  height++;
	  in_x = 1;

	  if (start_x == -1){
	    start_x=k;

	    fprintf(stderr, "start_x is defined; j=%d, k=%d, s[%d][%d]=%s, start_x=%d\n", j,k,i,j,s[i][j],start_x);

	    in_y = 1;
	  } else if (start_x != k){

	    fprintf(stderr, "diff in start_x; j=%d, k=%d, s[%d][%d]=%s\n", j,k,i,j,s[i][j]);
	    ans = 2;
	  }	    
	  
	  continue;
	}
	if(s[i][j][k] == '#' && in_x == 1) {
	  continue;
	}
	if(s[i][j][k] == '#' && in_x == 2) {
	  fprintf(stderr, "# after end of x; j=%d, k=%d, s[%d][%d]=%s\n", j,k,i,j,s[i][j]);
	  ans=2;
	}
      }

      if (in_x == 1 && end_x == -1){
	end_x = n[i]-1;

	fprintf(stderr, "end_x is defined; j=%d, s[%d][%d]=%s, end_x=%d\n", j,i,j,s[i][j],end_x);
      }

      if (in_x == 0 && in_y == 1){
	in_y = 2;
      }
    }

    fprintf(stderr, "height=%d, start_x=%d, end_x=%d\n", height, start_x, end_x);
    if (ans !=2 && height == end_x - start_x +1){
      ans = 1;
    }
    printf("Case #%d: %s\n", i+1, (ans == 1) ? "YES" : "NO");
  }
}
