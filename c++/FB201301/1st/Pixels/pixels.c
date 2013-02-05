#include <stdio.h>
#include <stdlib.h>

#define MAX_W  40000
#define MAX_N  1000000

#define FALSE 0
#define TRUE 1

typedef struct {
  int x, y;
} Pixel;

int t,cas;
int w,h,p,q,n,x,y,a,b,c,d;

Pixel dirty_pixel[MAX_N];
Pixel ysorted_pixel[MAX_N+2];
Pixel xsorted_pixel[MAX_N+2];

copy_pixel_pt(Pixel * from, Pixel * to){
  to->x=from->x;
  to->y=from->y;
}

copy_pixel(Pixel from, Pixel to){
  to.x=from.x;
  to.y=from.y;
}

copy_pixel_array(Pixel from[], Pixel to[], int num){
  int i;
  for(i=0; i<num; i++){
    copy_pixel(from[i], to[i]);
  }
}

int y_sort_cmp(const void* a, const void* b){
  Pixel pa = *(Pixel *) a;
  Pixel pb = *(Pixel *) b;
  return (pa.y - pb.y);
}

int x_sort_cmp(const void* a, const void* b){
  Pixel pa = *(Pixel *) a;
  Pixel pb = *(Pixel *) b;
  return (pa.x - pb.x);
}

void calc_dirty_pixel(){
  int i;

  dirty_pixel[0].x=x;
  dirty_pixel[0].y=y;

  for (i=1; i < n; i++){
    dirty_pixel[i].x = (dirty_pixel[i-1].x * a + dirty_pixel[i-1].y * b + 1) %w;
    dirty_pixel[i].y = (dirty_pixel[i-1].x * c + dirty_pixel[i-1].y * d + 1) %h;
  }
}

void calc_ysorted_pixel(){

  ysorted_pixel[0].x=-1;
  ysorted_pixel[0].y=-1;

  ysorted_pixel[n+1].x=w;
  ysorted_pixel[n+1].y=h;

  copy_pixel_array(&dirty_pixel[1], ysorted_pixel, n);

  qsort(&ysorted_pixel[0], n+2,sizeof(Pixel), y_sort_cmp);
}
    
void init_xsorted_pixel(){
  int i;
  for (i=0; i<n+2; i++){
    xsorted_pixel[i].x=0;
    xsorted_pixel[i].y=0;
  }
}

int calc_xsorted_pixel(int num){

  int i, ret;
  qsort(&xsorted_pixel[0], num, sizeof(Pixel), x_sort_cmp);
  ret =0;
  for(i=0; i<n+1; i++){
    int diff = xsorted_pixel[i+1].x - xsorted_pixel[i].x - p;
    if(diff > 0){
      ret += diff;
    }
  }
  return ret;
}

void init() {
  int i;
  for(i=0; i<n; i++){
    dirty_pixel[i].x=0;
    dirty_pixel[i].y=0;
    ysorted_pixel[i].x=0;
    ysorted_pixel[i].y=0;
    xsorted_pixel[i].x=0;
    xsorted_pixel[i].y=0;
  }
}

void read() {
    scanf("%d %d %d %d %d %d %d %d %d %d %d\n", &w,&h,&p,&q,&n,&x,&y,&a,&b,&c,&d);
    return;
}

int main() {

  int i, j, num_pixel;
  int ry, rx;
  int answer;

  scanf("%d\n", &t);

  for (cas=0; cas < t; cas++){

    //    answer=0;
    init();
    read();

    calc_dirty_pixel();
    calc_ysorted_pixel(); // sort & add (-1,-1), (W,H)
 
    int yi=0; int ye=0;

    while(yi<n+2){

      int ry = ysorted_pixel[yi].y;

      i=yi;
      while(ysorted_pixel[i].y == ry){
	i++;
      }
      ye = ysorted_pixel[i].y;

      i=yi; j=0;

      init_xsorted_pixel(); 
      
      while(ysorted_pixel[i].y >= ry && ysorted_pixel[i].y < ry+q){
	copy_pixel_pt(&ysorted_pixel[i++], &xsorted_pixel[j++]);
      }
      
      yi = i;      
      int xnum = calc_xsorted_pixel(j);// sort & calc sum

      answer += xnum * (ye - yi);

    }

    printf("Case #%d: %d\n", cas+1, answer);

  }
}
