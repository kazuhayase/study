import java.util.HashMap;
import java.util.HashSet;

public class BalancedSubstrings {

	
	public int calc (char[] str){
		int ret=0;
		String st = str.toString();
		if(calcResult.containsKey(st)){
			return calcResult.get(st);
		}
		
		for(int i=0; i<str.length; i++){
			ret += (i+1) * str[i];
		}

		Integer ca = new Integer(ret);
		calcResult.put(st, ca);
		return ret;
	}
	static HashMap <String, Integer> calcResult = new HashMap <String, Integer>();
	static HashSet <String> balanceString = new HashSet <String>();
	public boolean isBalanced(String s){
		if(balanceString.contains(s)){
			return true;
		}
		int len = s.length();
		for(int i=0; i < len -1; i++){
			char[] left = s.substring(0, i).toCharArray();
			char[] inLeft = new char[2500];
			for(int j=0; j < left.length; j++){
				inLeft[j]=left[left.length - j];
			}
			char[] right = s.substring(i+1, len-1).toCharArray();
			if(calc(inLeft)==calc(right)){
				balanceString.add(s);
				return true;
			}
		}
		return false;
	}
	
	public int countSubstrings(String s) {
		int len = s.length();
		int ret=0;
		for(int i=1; i<=len; i++){
			for(int j=0; j<len-i+1; j++){
				if(isBalanced(s.substring(j, j+i-1))){
					ret++;
				}
			}
		}
		return ret;
	}

}
