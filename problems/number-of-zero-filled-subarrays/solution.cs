public class Solution {
    public long ZeroFilledSubarray(int[] nums) {
        long count = 0;
        long total = 0;

        foreach (int num in nums) {
            if (num == 0) {
                count++;
                total += count;
            } else {
                count = 0;
            }
        }

        return total;
    }
}