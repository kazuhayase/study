public class LuckySum {

	public long construct(String note) {
		char[] cA = note.toCharArray();
		int[] iA = new int[20];

		if(cA[0]!='?' && cA[0]=='1' && cA[0] != '4' && cA[0] != '5' && cA[0] != '7' && cA[0] != '8'){
			return -1;
		}
		
		for(int i=1; i<cA.length; i++){
			
		}
		return 0;
	}

}
