public class Solution {
    public int MajorityElement(int[] nums) {
        if(nums.Length ==1) return nums[0];
        int count=0, res = nums[0];

        for(int i = 0; i< nums.Length; i++){
            if(count == 0 ){
                res = nums[i];
            }
            count += nums[i] == res?1:-1;
        }
        return res;
    }
}