import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class TheNumberGameTest {

    protected TheNumberGame solution;

    @Before
    public void setUp() {
        solution = new TheNumberGame();
    }

    @Test
    public void testCase0() {
        int A = 45;
        int B = 4;

        String expected = "Manao wins";
        String actual = solution.determineOutcome(A, B);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        int A = 45;
        int B = 5;

        String expected = "Manao wins";
        String actual = solution.determineOutcome(A, B);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        int A = 99;
        int B = 123;

        String expected = "Manao loses";
        String actual = solution.determineOutcome(A, B);

        Assert.assertEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        int A = 2356236;
        int B = 5666;

        String expected = "Manao loses";
        String actual = solution.determineOutcome(A, B);

        Assert.assertEquals(expected, actual);
    }

}
