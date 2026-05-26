public class Solution {
    public int SmallestDivisor(int[] nums, int threshold) {
        int low =1, high = nums.Max();
        return SearchDivisor(nums, threshold, low, high);
    }

    
private int SearchDivisor(int[] arr, int threshold, int low, int high) {
        if (low > high) {
            return low; 
        }

        int mid = low + (high - low) / 2;
        
        long currentSum = 0;
        for (int i = 0; i < arr.Length; i++) {
            currentSum += (long)Math.Ceiling((double)arr[i] / mid);
        }

        if (currentSum <= threshold) {
            return SearchDivisor(arr, threshold, low, mid - 1);
        } else {
            return SearchDivisor(arr, threshold, mid + 1, high);
        }
    }
}