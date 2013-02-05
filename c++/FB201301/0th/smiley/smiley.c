#include <stdio.h>
#include <string.h> 

#define MAX_T  50
#define MAX_S  100

int t;
char s[MAX_T][MAX_S];
int dp[MAX_S][MAX_S / 2];

void read();
void solve();

int main(){

  read();
  solve();
  return 0;

}

void dump(){
  int a,b;
  for (a=0; a < MAX_S; a++){
    printf("[%d]", a);
    for (b=0; b < MAX_S / 2 ; b++){
      printf("%d ", dp[a][b]);
    }
    printf("\n");
  }
}

int scan(int index, int value, int cas){

  /*
    if (dp[index][value] >= 2){
    return dp[index][value];
    }
    
  */

  if ( index == strlen(s[cas]) ) {
    if (value == 0){
      return 1;
    } else {
      return 0;
    }
    // return value == 0;
  }

  int i;
  for (i = index; i < strlen(s[cas]); i++){

    //right face
    if ( s[cas][i] == ':' && s[cas][i+1] ==')' ) { 
      if (value > 0) {
	
	// return dp[index][value] = (scan(i+2, value, cas) | scan(i+2, value-1, cas));
	return (scan(i+2, value, cas) | scan(i+2, value-1, cas) );
	
      } else {
	
	return scan(i+2, value, cas);
      }
    }

    //left face
    else if ( s[cas][i] == ':' && s[cas][i+1] =='(' ) {

      // return dp[index][value] = (scan(i+2, value, cas) | scan(i+2, value+1, cas));
      return (scan(i+2, value, cas) | scan(i+2, value+1, cas) );

    }

    else if ( s[cas][i] == ')' ) {
      if (value > 0){
	// return dp[index][value] = scan(i+1, value-1, cas);
	return scan(i+1, value-1, cas);
      } else {
	// return dp[index][value] = 0;
	return 0;
      }
    }
    else if ( s[cas][i] == '(' ) {
      // return dp[index][value] = scan(i+1, value+1, cas);
      return scan(i+1, value+1, cas);
    }
    
  }
}

void solve(){

  int i;
  for (i = 0; i < t; i++){

    printf("Case #%d: %s\n", i+1, scan(0,0,i) ? "YES" : "NO");

  }
}

// read from standard input
void read (){
  scanf("%d\n", &t);
  int i;
  for (i = 0; i < t; i++){
    gets(s[i]);
    //printf("%s\n", s[i]);
  }
}

