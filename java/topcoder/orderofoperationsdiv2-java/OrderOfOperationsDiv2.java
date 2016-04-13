public class OrderOfOperationsDiv2 {

	public int minTime(String[] s) {
		int n = s.length;
		int m = s[0].length();
		char[][] str = new char[n][m];
		for(int i=0; i<n; i++){
			str[i]=s[i].toCharArray();
		}
		int ret=0;
		for(;;){
			int min=m+1;
			int minX=-1;
			for(int i=0; i<n; i++){
				int cnt=0;
				for(int j=0; j<m; j++){
					if(str[i][j]=='1') cnt++;
				}
				if (cnt>0 && min>cnt){
					min = cnt;
					minX=i;
				}
			}
			if(min==m+1){
				return ret;
			} else {
				ret += min*min;
				for(int j=0; j<m; j++){
					if(str[minX][j]=='1'){
						for(int i=0; i<n; i++){
							str[i][j]='0';							
						}	
					}
				}
			}
		}
	}
}
