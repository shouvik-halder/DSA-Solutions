public class Solution {
    public int RemoveDuplicates(int[] nums) {
        if (nums.Length <= 2)
        return nums.Length;

        int n = nums.Length, x = 2;
        for(int i=2;i<n;i++){
            if(nums[i]!=nums[x-2]){
                nums[x] = nums[i];
                x++;
            }
        }
        return x;
    }
}