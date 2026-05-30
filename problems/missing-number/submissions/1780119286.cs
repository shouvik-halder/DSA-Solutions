public class Solution {
    public int MissingNumber(int[] nums) {
        int n = nums.Length;
        int sum = n*(n+1)/2;
        for(int i = 0; i<n;i++){
            sum-=nums[i];
        }
        return sum;
    }
}