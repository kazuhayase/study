#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_M  50
#define MAX_K  101
#define FALSE 0
#define TRUE 1

typedef struct ind_string {
  char str[MAX_K];
  int index;
} index_string;

int t,cas,m,l,L;
char k1[MAX_K],k2[MAX_K],k[MAX_K];
index_string replg[MAX_M][MAX_M]; // foreach fi, replace matched g in minimum lex + add "index of g"
int matched[MAX_M]; //number of matched g for each f
int used[MAX_M];
//int fg[MAX_M][MAX_M];

void print_replg(){
  int i,j;
  for (i=0; i<m; i++){
    printf("[%d]",i);
    for (j=0; j<matched[i]; j++){
      printf("[%s][%d]", replg[i][j].str, replg[i][j].index);
    }
    printf("\n");
  }
}


int sort_cmp(const void* a, const void* b){
  return strncmp(a , b, l);
}

void read() {
    scanf("%d\n", &m);
    scanf("%s\n", k1);
    scanf("%s\n", k2);
    L = strlen(k1);
    l = strlen(k1) / m;
    return;
}

int check_word(int fi, int gi, int replgi) {

  int j;
  for (j=0; j < l; j++){
    char fc=k1[fi * l + j];
    char gc=k2[gi * l + j];
    if (fc == '?') {
      if (gc == '?'){
	replg[fi][replgi].str[j] = 'a';
      }
      else replg[fi][replgi].str[j] = gc;
    } else if (gc == '?' || fc == gc){
      replg[fi][replgi].str[j] = fc; 
    } else {
      return FALSE;
    }
  }
  replg[fi][replgi].index = gi;
  return TRUE;
}

void sort_fg(int fi, int replgi){

  qsort(&replg[fi][0].str[0], replgi, sizeof(index_string), sort_cmp);

}

void match(int fi){

  int fgi=0, matching=0, gi;
  for (gi=0; gi < m; gi++){  
    if(check_word (fi, gi, matching)){
      //fg[fi][fgi++]=gi;
      matching++;
    }
  }

  matched[fi] = matching;

  //print_replg();

  sort_fg(fi,matching);

  //print_replg();

}

int try(int fi){
  if(fi == m) return TRUE;
  int flag =0, j;
  for (j=0; j < matched[fi]; j++){
    int using = replg[fi][j].index;
    if (used[using] == FALSE){
      used[using] = TRUE;
      if (try(fi+1)){
	int iii;
	for(iii=0; iii<l; iii++){
	  k[fi*l+iii]=replg[fi][j].str[iii];
	}
	return TRUE;
      } else {
	used[using] = FALSE;
      }
    } else {;}
  }
  return FALSE;
}

void init() {
  int i,j;

  for(i=0; i<MAX_K; i++){
    k[i]='\0';
  }

  for(i=0; i<MAX_M; i++){
    matched[i]=0;
    for(j=0; j<MAX_M; j++){    
      //fg[i][j] = -1;
    }
  }
}

int main() {

  int i,fi,j,jj;

  scanf("%d\n", &t);

  for (cas=0; cas < t; cas++){

    init();
    read();

    for (i=0; i < m; i++){
      match(i);
    }

    //print_replg();

    for (j=0; j < m; j++){
      used[j] = FALSE;
    }

    if (try(0)){

      k[L+1] = '0';

      printf("Case #%d: %s\n", cas+1, k);
    } else {
      printf("Case #%d: IMPOSSIBLE\n", cas+1);
    }
  }
}
