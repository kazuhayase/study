#include <cstdio>
#include <algorithm>
#include <string> 
#include <cstring> 

/*
std::string data = "Abc"; 
std::transform(data.begin(), data.end(), data.begin(), ::tolower);
*/

const int Alpha = 25;
const int MAX_M = 50;
const int MAX_S = 501;


int m, score[MAX_M], count[Alpha];
char s[MAX_M][MAX_S];

void read();
void solve();

int main(){

  read();
  solve();
  return 0;

}

void solve(){

  // quad loop
  for (int i = 0; i < m; i++){

    for(int a = 0; a < Alpha; a++) {
      count[a] = 0;
    }

    for (int j = 0; j < strlen(s[i]); j++){
      int l;
      if (s[i][j] >='a' && s[i][j] <= 'z') {
	l = s[i][j] - 'a';
	count[l]++;
      } else if (s[i][j] >='A' && s[i][j] <= 'Z') {
	l = s[i][j] - 'A';
	count[l]++;
      } 

    }

    std::sort (count, count+Alpha, std::greater<int>() );
    
    for (int j = 0; j < Alpha; j++){
      int beauty = 26 - j;
      if (count[j] > 0){ 
	score[i] += beauty*count[j];
      }
    }
   // write to standard output
    printf("Case #%d: %d\n", i+1, score[i]);
  }
      
}

// read from standard input
void read (){
  scanf("%d\n", &m);
  for (int i = 0; i < m; i++){
    // scanf("%[^\n]", s[i]);
    //std::getline(std::ios, s[i]);
    gets(s[i]);
    //printf("%s\n", s[i]);
  }
}
