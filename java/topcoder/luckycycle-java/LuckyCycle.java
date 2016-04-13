public class LuckyCycle {

	public int[] getEdge(int[] edge1, int[] edge2, int[] weight) {
		int[][] edge = new int[100][100];
		int nodes = edge1.length + 1;
		
		for(int i=0; i<edge1.length; i++){
			if(edge1[i]>edge2[i]){
				int tmp=edge1[i];
				edge1[i]=edge2[i];
				edge2[i]=tmp;
			}
		}
		
		for(int i=0; i<edge1.length; i++){
			for(int j=0; j<edge1.length; j++){
				int v1=-1, v2=-1;
				if(i!=j && weight[i]!=weight[j] && 
						(edge1[i] == edge1[j] || edge1[i] == edge2[j] || edge2[i] == edge1[j] || edge2[i] == edge2[j])	){
						if(edge1[i]<edge1[j]){
							if(edge2[i]==edge1[j]){
								v1=edge1[i]; v2=edge2[j];
							} else {
								v1=edge1[i]; v2=edge1[j];
							}
						} else if(edge1[i]==edge1[j]){
							v1=edge2[i]; v2=edge2[j];
						} else {
							if(edge2[j]==edge1[i]){
								v1=edge2[i]; v2=edge1[j];
							} else {
								v1=edge2[i]; v2=edge2[j];
							}
						}
						for(int k=0; k<edge1.length; k++){
							if(i!=k && j!=k){
							if(weight[i]!=weight[k] &&
								(edge1[i] == edge1[k] || edge1[i] == edge2[k] || edge2[i] == edge1[k] || edge2[i] == edge2[k])	){
								int[] ret = {
							}
						
				}
			}
		}
	return null;
	}

}
