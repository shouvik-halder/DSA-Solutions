public class Solution {
    public bool Check(int[] nums) {
        int isInverted=0;
        for(int i=1;i<nums.Length;i++){
            if(nums[i]<nums[i-1]){
                ++isInverted;
            }
            if(isInverted>1) return false;
        }
        if(nums[0]<nums[nums.Length-1]) ++isInverted;
        return isInverted<=1;
    }
}