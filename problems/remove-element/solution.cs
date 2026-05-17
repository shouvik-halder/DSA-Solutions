public class Solution {
    public int RemoveElement(int[] nums, int val) {
        int n = nums.Length, k=0;

        for(int i = 0;i<n;i++){
            if(nums[i]!=val){
                if(i!=k){
                    (nums[i], nums[k])=(nums[k], nums[i]);
                }
                k++;
            }
        }
        return k;
    }
}