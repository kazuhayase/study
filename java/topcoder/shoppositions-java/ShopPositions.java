public class ShopPositions {

	public int maxProfit(int n, int m, int[] c) {
		int[][][] count = new int[n][m+1][m+1];
		for(int j=1; j<=m; j++){
			for(int k=0; k<=m; k++){
				count[0][j][k] = j * c[j+k-1];
			}
		}
		for(int i=1; i<n-1; i++){
			for(int k=0; k<=m; k++){
				int max=0;
				int maxL=0;
				for(int l=0; l<=m; l++){
					int cnt = count[i-1][l][0];
					if(max<cnt){
						max=cnt;
						maxL=l;
					}
				}
				count[i][0][k] = count[i-1][maxL][0] + max; 					
			}
			for(int j=1; j<=m; j++){
				for(int k=0; k<=m; k++){
					int max=0;
					int maxL=0;
					for(int l=0; l<=m; l++){
						int cnt = count[i-1][l][j] + j * c[i*3*(l+j+k)+j-1];
						if(max<cnt){
							max=cnt;
							maxL=l;
						}
					}
					count[i][j][k] = count[i-1][maxL][j] + max; 					
				}
			}
		}
		int ret=0;
		if(n>1){
		for(int j=0; j<=m; j++){
			int max=0;
			int maxL=0;
			for(int l=0; l<=m; l++){
				int cnt = count[n-2][l][j] + j * c[(n-2)*3*(l+j)+j];
				if(max<cnt){
					max=cnt;
					maxL=l;
				}
				count[n-1][j][0] = count[n-2][maxL][j] + max;
				if (ret < count[n-1][j][0]){
					ret = count[n-1][j][0];
				}
			}
		}
		} else {
			for(int j=0; j<=m; j++){
				if(ret < count[0][j][0]){
					ret = count[0][j][0];
				}
			}
		}
		return ret;
	}
}
