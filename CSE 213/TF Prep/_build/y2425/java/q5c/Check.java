public class Check {
    static int gcd(int a, int b) {
        long x = Math.abs((long) a);
        long y = Math.abs((long) b);
        while (y != 0) { long temp = y; y = x % y; x = temp; }
        return (int) x;
    }
    public static void main(String[] s) {
        int[][] t = {{12,18,6},{18,12,6},{-12,18,6},{12,-18,6},{-12,-18,6},{0,0,0},{0,5,5},{5,0,5},{0,-5,5},{-5,0,5},
                     {7,7,7},{-7,7,7},{17,13,1},{12,4,4},{4,12,4},{1,99,1},{99,1,1},{-1,0,1},{1071,462,21},
                     {2147483647,2147483647,2147483647},{2147483647,1,1},{2147483647,2147483646,1},{1000000007,998244353,1},
                     {46368,75025,1},{1<<30,1<<20,1<<20},{Integer.MIN_VALUE,2,2},{Integer.MIN_VALUE,6,2},{Integer.MIN_VALUE,Integer.MAX_VALUE,1}};
        boolean ok = true;
        for (int[] r : t) {
            int g = gcd(r[0], r[1]);
            if (g != r[2]) { ok = false; System.out.println("MISMATCH gcd(" + r[0] + "," + r[1] + ") = " + g + " expected " + r[2]); }
        }
        System.out.println("table ok = " + ok);
        System.out.println("gcd(MIN,0) = " + gcd(Integer.MIN_VALUE, 0) + "   gcd(0,MIN) = " + gcd(0, Integer.MIN_VALUE)
                + "   gcd(MIN,MIN) = " + gcd(Integer.MIN_VALUE, Integer.MIN_VALUE));
    }
}
