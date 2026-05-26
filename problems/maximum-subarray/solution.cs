public class Solution {
    public int MaxSubArray(int[] nums) {
        int sum=0, maxSum=nums[0];
        for(int i=0;i<nums.Length;i++){
            sum=Math.Max(sum+nums[i],nums[i]);
            maxSum=Math.Max(maxSum,sum);
        }
        return maxSum;
    }
}