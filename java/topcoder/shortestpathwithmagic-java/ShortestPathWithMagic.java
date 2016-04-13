import java.util.Arrays;

public class ShortestPathWithMagic {

	
	public double getTime(String[] dist, int k) {
		boolean[] used = new boolean[50];
		int[] d = new int[50];
		int[] prev = new int[50];
		int[][] e = new int[50][50];
		int num =0;
		
		num = dist.length;
		d[0]=0;

		for(int i=0; i<num; i++){
			char[] tmp = dist[i].toCharArray();
			for(int j=0; j<num; j++){
				e[i][j] = tmp[j] - '0';
			}
			used[i]=false;
			d[i]=10000;
			prev[i]=-1;
		}
		
		while(true){
			int v=-1;
			for(int u=0; u<num; u++){
				if(!used[u] && (v==-1 || d[u] < d[v])){
					v = u;
				}
			}
			if (v == -1) break;
			used[v]=true;
			for(int u=0; u<num; u++){
				if(d[u]>d[v]+e[v][u]){
					d[u] = d[v] + e[v][u];
					prev[u]=v;
				}
			}
		}
		int u=1;
		int[] path = new int[50];
		int i=0;
		for(i=0; i<50; i++){
			path[i]=e[u][prev[u]];
			u=prev[u];
			if(u==0) break;
		}
		Arrays.sort(path);
		double res=0;
		for(int j=0; j<=i; j++){
			if(j<k){
				res += path[49-j]/2;
			} else {
				res += path[49-j];
			}
		}
		return res;
	}

}
