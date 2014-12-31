// BEGIN CUT HERE
// PROBLEM STATEMENT
// Let's say you have a binary string such as the following:

/*
011100011

One way to encrypt this string is to add to each digit the sum of its adjacent digits.  For example, the above string would become:

123210122

In particular, if P is the original string, and Q is the encrypted string, then Q[i] = P[i-1] + P[i] + P[i+1] for all digit positions i.  Characters off the left and right edges of the string are treated as zeroes.

An encrypted string given to you in this format can be decoded as follows (using 123210122 as an example):

Assume P[0] = 0.
Because Q[0] = P[0] + P[1] = 0 + P[1] = 1, we know that P[1] = 1.
Because Q[1] = P[0] + P[1] + P[2] = 0 + 1 + P[2] = 2, we know that P[2] = 1.
Because Q[2] = P[1] + P[2] + P[3] = 1 + 1 + P[3] = 3, we know that P[3] = 1.
Repeating these steps gives us P[4] = 0, P[5] = 0, P[6] = 0, P[7] = 1, and P[8] = 1.
We check our work by noting that Q[8] = P[7] + P[8] = 1 + 1 = 2.  Since this equation works out, we are finished, and we have recovered one possible original string.

Now we repeat the process, assuming the opposite about P[0]:

Assume P[0] = 1.
Because Q[0] = P[0] + P[1] = 1 + P[1] = 1, we know that P[1] = 0.
Because Q[1] = P[0] + P[1] + P[2] = 1 + 0 + P[2] = 2, we know that P[2] = 1.
Now note that Q[2] = P[1] + P[2] + P[3] = 0 + 1 + P[3] = 3, which leads us to the conclusion that P[3] = 2.  However, this violates the fact that each character in the original string must be '0' or '1'.  Therefore, there exists no such original string P where the first digit is '1'.

Note that this algorithm produces at most two decodings for any given encrypted string.  There can never be more than one possible way to decode a string once the first binary digit is set.

Given a String message, containing the encrypted string, return a String[] with exactly two elements.  The first element should contain the decrypted string assuming the first character is '0'; the second element should assume the first character is '1'.  If one of the tests fails, return the string "NONE" in its place.  For the above example, you should return {"011100011", "NONE"}.

DEFINITION
Class:BinaryCode
Method:decode
Parameters:String
Returns:String[]
Method signature:String[] decode(String message)


CONSTRAINTS
-message will contain between 1 and 50 characters, inclusive.
-Each character in message will be either '0', '1', '2', or '3'.


EXAMPLES

0)
"123210122"

Returns: { "011100011",  "NONE" }

The example from above.

1)
"11"

Returns: { "01",  "10" }

We know that one of the digits must be '1', and the other must be '0'.  We return both cases.

2)
"22111"

Returns: { "NONE",  "11001" }

Since the first digit of the encrypted string is '2', the first two digits of the original string must be '1'.  Our test fails when we try to assume that P[0] = 0.

3)
"123210120"

Returns: { "NONE",  "NONE" }

This is the same as the first example, but the rightmost digit has been changed to something inconsistent with the rest of the original string.  No solutions are possible.

4)
"3"

Returns: { "NONE",  "NONE" }

5)
"12221112222221112221111111112221111"

Returns: { "01101001101101001101001001001101001",  "10110010110110010110010010010110010" }
*/
// END CUT HERE
import java.util.*;
public class BinaryCode {
    public String[] decode(String message) {

	String[] answer = new String[2];
	int[] buffer = new int[100];
	int length = message.length();
	boolean flag;

	for(int j=0; j<2; j++){
	    flag = true;
	    answer[j] = "";
	    buffer[0] = j; 
	    buffer[1] = Character.getNumericValue(message.charAt(0)) - buffer[0];
	    if ((buffer[1] != 0) && (buffer[1] != 1)){
		flag = false;
	    }
	    for(int i=1; i<length-1; i++){
		buffer[i+1] = Character.getNumericValue(message.charAt(i)) - buffer[i] - buffer[i-1];
		if ((buffer[i+1] != 0) && (buffer[i+1] != 1)){
		    flag = false;
		}
	    }
	    // check last character
	    if(flag && Character.getNumericValue(message.charAt(length-1)) != buffer[length-2] + buffer[length-1]){
		flag = false;
	    }

	    if(flag){
		for(int i=0; i<length; i++){
		    answer[j] += String.valueOf(buffer[i]);
		}
	    } else {
		answer[j] = "NONE";
	    }
	}
	return answer;
    }
    
    

// BEGIN CUT HERE
    public static void main(String[] args) {
        try {
            eq(0,(new BinaryCode()).decode("123210122"),new String[] { "011100011",  "NONE" });
            eq(1,(new BinaryCode()).decode("11"),new String[] { "01",  "10" });
            eq(2,(new BinaryCode()).decode("22111"),new String[] { "NONE",  "11001" });
            eq(3,(new BinaryCode()).decode("123210120"),new String[] { "NONE",  "NONE" });
            eq(4,(new BinaryCode()).decode("3"),new String[] { "NONE",  "NONE" });
            eq(5,(new BinaryCode()).decode("12221112222221112221111111112221111"),new String[] { "01101001101101001101001001001101001",  "10110010110110010110010010010110010" });
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

