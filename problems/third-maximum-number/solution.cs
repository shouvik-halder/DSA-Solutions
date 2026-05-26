public class Solution {
    public int ThirdMax(int[] nums) {
        // Use long to avoid sentinel collision with int.MinValue
        long first = long.MinValue;
        long second = long.MinValue;
        long third = long.MinValue;

        foreach (int num in nums) {
            // Skip duplicates
            if (num == first || num == second || num == third) {
                continue;
            }
            if (num > first) {
                // New largest: shift everything down
                third = second;
                second = first;
                first = num;
            } else if (num > second) {
                // New second largest: shift third down
                third = second;
                second = num;
            } else if (num > third) {
                // New third largest
                third = num;
            }
        }

        // If third was never assigned, return the maximum
        return (int)(third == long.MinValue ? first : third);
    }
}