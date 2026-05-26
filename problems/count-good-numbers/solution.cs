public class Solution {
     private const long MOD = 1_000_000_007;

    public int CountGoodNumbers(long n) {
        long evenPositions = (n + 1) / 2;
        long oddPositions = n / 2;

        long countEvenChoices = Power(5, evenPositions);
        long countOddChoices = Power(4, oddPositions);

        long result = (countEvenChoices * countOddChoices) % MOD;

        return (int)result;
    }

    private long Power(long baseNum, long exp) {
        long res = 1;
        baseNum %= MOD; 

        while (exp > 0) {
            if (exp % 2 == 1) {
                res = (res * baseNum) % MOD;
            }
            baseNum = (baseNum * baseNum) % MOD;
            exp /= 2;
        }
        return res;
    }
}