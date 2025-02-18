/*
// BEGIN CUT HERE
// PROBLEM STATEMENT

// In most states, gamblers can choose from a wide variety of different lottery games.  The rules of a lottery are defined by two integers (choices and blanks) and two boolean variables (sorted and unique).  choices represents the highest valid number that you may use on your lottery ticket.  (All integers between 1 and choices, inclusive, are valid and can appear on your ticket.)  blanks represents the number of spots on your ticket where numbers can be written.

The sorted and unique variables indicate restrictions on the tickets you can create.  If sorted is set to true, then the numbers on your ticket must be written in non-descending order.  If sorted is set to false, then the numbers may be written in any order.  Likewise, if unique is set to true, then each number you write on your ticket must be distinct.  If unique is set to false, then repeats are allowed.

Here are some example lottery tickets, where choices = 15 and blanks = 4:
{3, 7, 12, 14} -- this ticket is unconditionally valid.
{13, 4, 1, 9} -- because the numbers are not in nondescending order, this ticket is valid only if sorted = false.
{8, 8, 8, 15} -- because there are repeated numbers, this ticket is valid only if unique = false.
{11, 6, 2, 6} -- this ticket is valid only if sorted = false and unique = false.

Given a list of lotteries and their corresponding rules, return a list of lottery names sorted by how easy they are to win.  The probability that you will win a lottery is equal to (1 / (number of valid lottery tickets for that game)).  The easiest lottery to win should appear at the front of the list.  Ties should be broken alphabetically (see example 1).

DEFINITION
Class:Lottery
Method:sortByOdds
Parameters:String[]
Returns:String[]
Method signature:String[] sortByOdds(String[] rules)


CONSTRAINTS
-rules will contain between 0 and 50 elements, inclusive.
-Each element of rules will contain between 11 and 50 characters, inclusive.
-Each element of rules will be in the format "<NAME>:_<CHOICES>_<BLANKS>_<SORTED>_<UNIQUE>" (quotes for clarity). The underscore character represents exactly one space. The string will have no leading or trailing spaces.
-<NAME> will contain between 1 and 40 characters, inclusive, and will consist of only uppercase letters ('A'-'Z') and spaces (' '), with no leading or trailing spaces.
-<CHOICES> will be an integer between 10 and 100, inclusive, with no leading zeroes.
-<BLANKS> will be an integer between 1 and 8, inclusive, with no leading zeroes.
-<SORTED> will be either 'T' (true) or 'F' (false).
-<UNIQUE> will be either 'T' (true) or 'F' (false).
-No two elements in rules will have the same name.


EXAMPLES

0)
{"PICK ANY TWO: 10 2 F F"
,"PICK TWO IN ORDER: 10 2 T F"
,"PICK TWO DIFFERENT: 10 2 F T"
,"PICK TWO LIMITED: 10 2 T T"}

Returns: { "PICK TWO LIMITED",  "PICK TWO IN ORDER",  "PICK TWO DIFFERENT",  "PICK ANY TWO" }

The "PICK ANY TWO" game lets either blank be a number from 1 to 10.  Therefore, there are 10 * 10 = 100 possible tickets, and your odds of winning are 1/100.

The "PICK TWO IN ORDER" game means that the first number cannot be greater than the second number.  This eliminates 45 possible tickets, leaving us with 55 valid ones.  The odds of winning are 1/55.

The "PICK TWO DIFFERENT" game only disallows tickets where the first and second numbers are the same.  There are 10 such tickets, leaving the odds of winning at 1/90.

Finally, the "PICK TWO LIMITED" game disallows an additional 10 tickets from the 45 disallowed in "PICK TWO IN ORDER".  The odds of winning this game are 1/45.

1)
{"INDIGO: 93 8 T F",
 "ORANGE: 29 8 F T",
 "VIOLET: 76 6 F F",
 "BLUE: 100 8 T T",
 "RED: 99 8 T T",
 "GREEN: 78 6 F T",
 "YELLOW: 75 6 F F"}


Returns: { "RED",  "ORANGE",  "YELLOW",  "GREEN",  "BLUE",  "INDIGO",  "VIOLET" }

Note that INDIGO and BLUE both have the exact same odds (1/186087894300).  BLUE is listed first because it comes before INDIGO alphabetically.

2)
{}

Returns: { }

Empty case

// END CUT HERE
*/

import java.util.*;
import java.util.regex.*;
import java.math.*;
public class Lottery {
    public String[] sortByOdds(String[] rules) {
        String[] res;

	SortedMap <BigInteger, SortedSet <String> > numToName = new TreeMap <BigInteger, SortedSet <String> >();
	
	/*
	String strName = "\\p{Upper}(\\p{Upper}| )*\\p{Upper}";
	String strChoices = "\\d+";
	*/

	String strName = "[A-Z](?:[A-Z]| )*[A-Z]";
	String strChoices = "[0-9]+";

	String strBlanks = "[1-8]";
	String strFlag ="[TF]"; // sorted & unique
	String strPattern = "(" + strName +"): (" + strChoices + ") (" + strBlanks + ") (" + strFlag + ") (" + strFlag + ")";


	//System.err.println("strPattern = '" + strPattern + "'");

	Pattern p = Pattern.compile(strPattern);
	
	Iterator itr = Arrays.asList(rules).iterator();
	//int numRules = 0;
	//String[] names = new String[50];
	//BigInteger[] tickets = new BigInteger[50];
	while(itr.hasNext()){
	    String item = itr.next().toString();
	    //System.err.println("item = " + item);
	    Matcher m = p.matcher(item);
	    if(m.find()){
		String name = m.group(1);
		//names[numRules] = m.group(1);
		BigInteger choices = new BigInteger(m.group(2));
		BigInteger Blanks = new BigInteger(m.group(3));
		int blanks = Integer.parseInt(m.group(3));
		boolean sorted = m.group(4).equals("T");
		boolean unique = m.group(5).equals("T");
		
		BigInteger ticket;
		BigInteger total = choices.pow(blanks);
		BigInteger perm = combi(choices, blanks);
		if(unique && sorted){
		    ticket = perm;
		} else if (!unique && sorted){
		    //ticket = total.subtract(perm);
		    ticket = combi(choices.add(Blanks).subtract(BigInteger.ONE), blanks);
		} else if (unique && !sorted){
		    ticket = factorCount(choices, blanks);
		} else {
		    ticket = total;
		}

		if(numToName.containsKey(ticket)){
		    numToName.get(ticket).add(name);
		} else {
		    SortedSet <String> lotNames = new TreeSet <String>();
		    lotNames.add(name);
		    numToName.put(ticket, lotNames);
		}
	    }
	}
	List <String> resList = new ArrayList <String> ();
	for (BigInteger keyNum : numToName.keySet()){
	    for (String lotName : numToName.get(keyNum)){
		resList.add(lotName);
	    }
	}
        //String[] res = resList.toArray(new String[resList.size()]);
        res = resList.toArray(new String[0]);
        return res;
    }

    BigInteger combi(BigInteger num, int count){
	BigInteger res = factorCount(num, count).divide(factor(count));
	return res;
    }

    BigInteger factor(int num){
	BigInteger res = new BigInteger("1");
	for(int i=num; i>0; i--){
	    res = res.multiply(BigInteger.valueOf(i));
	}
	return res;
    }

    BigInteger factorCount(BigInteger num, int count){
	BigInteger res = new BigInteger("1");
	while(count>0){
	    res = res.multiply(num);
	    num = num.subtract(BigInteger.ONE);
	    count--;
	}
	return res;
    }

// BEGIN CUT HERE
    public static void main(String[] args) {
        try {
            eq(0,(new Lottery()).sortByOdds(new String[] {"PICK ANY TWO: 10 2 F F"
               ,"PICK TWO IN ORDER: 10 2 T F"
               ,"PICK TWO DIFFERENT: 10 2 F T"
               ,"PICK TWO LIMITED: 10 2 T T"}),new String[] { "PICK TWO LIMITED",  "PICK TWO IN ORDER",  "PICK TWO DIFFERENT",  "PICK ANY TWO" });
            eq(1,(new Lottery()).sortByOdds(new String[] {"INDIGO: 93 8 T F",
                "ORANGE: 29 8 F T",
                "VIOLET: 76 6 F F",
                "BLUE: 100 8 T T",
                "RED: 99 8 T T",
                "GREEN: 78 6 F T",
                "YELLOW: 75 6 F F"}
               ),new String[] { "RED",  "ORANGE",  "YELLOW",  "GREEN",  "BLUE",  "INDIGO",  "VIOLET" });
            eq(2,(new Lottery()).sortByOdds(new String[] {}),new String[] { });
        } catch( Exception exx) {
            System.err.println(exx);
            exx.printStackTrace(System.err);
        }
    }
    private static void eq( int n, int a, int b ) {
        if ( a==b )
            System.err.println("Case "+n+" passed.");
        else
            System.err.println("Case "+n+" failed: expected "+b+", received "+a+".");
    }
    private static void eq( int n, char a, char b ) {
        if ( a==b )
            System.err.println("Case "+n+" passed.");
        else
            System.err.println("Case "+n+" failed: expected '"+b+"', received '"+a+"'.");
    }
    private static void eq( int n, long a, long b ) {
        if ( a==b )
            System.err.println("Case "+n+" passed.");
        else
            System.err.println("Case "+n+" failed: expected \""+b+"L, received "+a+"L.");
    }
    private static void eq( int n, boolean a, boolean b ) {
        if ( a==b )
            System.err.println("Case "+n+" passed.");
        else
            System.err.println("Case "+n+" failed: expected "+b+", received "+a+".");
    }
    private static void eq( int n, String a, String b ) {
        if ( a != null && a.equals(b) )
            System.err.println("Case "+n+" passed.");
        else
            System.err.println("Case "+n+" failed: expected \""+b+"\", received \""+a+"\".");
    }
    private static void eq( int n, int[] a, int[] b ) {
        if ( a.length != b.length ) {
            System.err.println("Case "+n+" failed: returned "+a.length+" elements; expected "+b.length+" elements.");
            return;
        }
        for ( int i= 0; i < a.length; i++)
            if ( a[i] != b[i] ) {
                System.err.println("Case "+n+" failed. Expected and returned array differ in position "+i);
                print( b );
                print( a );
                return;
            }
        System.err.println("Case "+n+" passed.");
    }
    private static void eq( int n, long[] a, long[] b ) {
        if ( a.length != b.length ) {
            System.err.println("Case "+n+" failed: returned "+a.length+" elements; expected "+b.length+" elements.");
            return;
        }
        for ( int i= 0; i < a.length; i++ )
            if ( a[i] != b[i] ) {
                System.err.println("Case "+n+" failed. Expected and returned array differ in position "+i);
                print( b );
                print( a );
                return;
            }
        System.err.println("Case "+n+" passed.");
    }
    private static void eq( int n, String[] a, String[] b ) {
        if ( a.length != b.length) {
            System.err.println("Case "+n+" failed: returned "+a.length+" elements; expected "+b.length+" elements.");
            return;
        }
        for ( int i= 0; i < a.length; i++ )
            if( !a[i].equals( b[i])) {
                System.err.println("Case "+n+" failed. Expected and returned array differ in position "+i);
                print( b );
                print( a );
                return;
            }
        System.err.println("Case "+n+" passed.");
    }
    private static void print( int a ) {
        System.err.print(a+" ");
    }
    private static void print( long a ) {
        System.err.print(a+"L ");
    }
    private static void print( String s ) {
        System.err.print("\""+s+"\" ");
    }
    private static void print( int[] rs ) {
        if ( rs == null) return;
        System.err.print('{');
        for ( int i= 0; i < rs.length; i++ ) {
            System.err.print(rs[i]);
            if ( i != rs.length-1 )
                System.err.print(", ");
        }
        System.err.println('}');
    }
    private static void print( long[] rs) {
        if ( rs == null ) return;
        System.err.print('{');
        for ( int i= 0; i < rs.length; i++ ) {
            System.err.print(rs[i]);
            if ( i != rs.length-1 )
                System.err.print(", ");
        }
        System.err.println('}');
    }
    private static void print( String[] rs ) {
        if ( rs == null ) return;
        System.err.print('{');
        for ( int i= 0; i < rs.length; i++ ) {
            System.err.print( "\""+rs[i]+"\"" );
            if( i != rs.length-1)
                System.err.print(", ");
        }
        System.err.println('}');
    }
    private static void nl() {
        System.err.println();
    }
// END CUT HERE
}
