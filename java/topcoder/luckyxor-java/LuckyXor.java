public class LuckyXor {

	public int construct(int a) {
		int[] luck = {4,7,44,47,74,77};
		for(int i=0; i<luck.length; i++){
			int b = a ^ luck[i];
			if(b>a && b>0 && b<100){
				return b;
			}
		}
		return -1;
	}

}
