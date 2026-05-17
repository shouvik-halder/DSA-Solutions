public class Solution {
    public int RemoveDuplicates(int[] nums) {
        int x = 0, n = nums.Length;
        for(int i=0;i<n;i++){
            if(nums[x]!=nums[i]){
                x+=1;
                nums[x] = nums[i];
            }
        }
        return x+1;
    }
}