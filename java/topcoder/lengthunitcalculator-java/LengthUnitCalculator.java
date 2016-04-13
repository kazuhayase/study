public class LengthUnitCalculator {

	public double calc(int amount, String fromUnit, String toUnit) {
		String[] unit = {"in", "ft", "yd", "mi"};
		int rate[] = {1, 12, 12*3, 12*3*1760};
		int fRate=1;
		int tRate=1;
		for(int i=0; i<4; i++){
			if(fromUnit.equals(unit[i])){
				fRate=rate[i];
			}
			if(toUnit.equals(unit[i])){
				tRate=rate[i];
			}
		}
		
		return amount * (double) fRate / (double) tRate;
	}

}
