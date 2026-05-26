public class Solution {
    public int FindMaxConsecutiveOnes(int[] nums) {
        int max=0, curr = 0, n = nums.Length;
        for(int i=0;i<n;i++){
            if(nums[i]!=1){
                if(curr>max){
                    max = curr;
                }
                curr=0;
            }
            else{
                curr++;
            }
        }
        return curr>max?curr:max;
    }
}