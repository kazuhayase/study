import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class LengthUnitCalculatorTest {

    protected LengthUnitCalculator solution;

    @Before
    public void setUp() {
        solution = new LengthUnitCalculator();
    }

    public static void assertEquals(double expected, double actual) {
        if (Double.isNaN(expected)) {
            Assert.assertTrue("expected: <NaN> but was: <" + actual + ">", Double.isNaN(actual));
            return;
        }
        double delta = Math.max(1e-9, 1e-9 * Math.abs(expected));
        Assert.assertEquals(expected, actual, delta);
    }

    @Test
    public void testCase0() {
        int amount = 1;
        String fromUnit = "mi";
        String toUnit = "ft";

        double expected = 5280.0;
        double actual = solution.calc(amount, fromUnit, toUnit);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase1() {
        int amount = 1;
        String fromUnit = "ft";
        String toUnit = "mi";

        double expected = 1.893939393939394E-4;
        double actual = solution.calc(amount, fromUnit, toUnit);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase2() {
        int amount = 123;
        String fromUnit = "ft";
        String toUnit = "yd";

        double expected = 41.0;
        double actual = solution.calc(amount, fromUnit, toUnit);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase3() {
        int amount = 1000;
        String fromUnit = "mi";
        String toUnit = "in";

        double expected = 6.336E7;
        double actual = solution.calc(amount, fromUnit, toUnit);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase4() {
        int amount = 1;
        String fromUnit = "in";
        String toUnit = "mi";

        double expected = 1.5782828282828283E-5;
        double actual = solution.calc(amount, fromUnit, toUnit);

        assertEquals(expected, actual);
    }

    @Test
    public void testCase5() {
        int amount = 47;
        String fromUnit = "mi";
        String toUnit = "mi";

        double expected = 47.0;
        double actual = solution.calc(amount, fromUnit, toUnit);

        assertEquals(expected, actual);
    }

}
