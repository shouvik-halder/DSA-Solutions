public class Solution {
    public int[] RearrangeArray(int[] nums) {
        int pos=0,neg=1;int[] res = new int[nums.Length];
        for(int i=0;i<nums.Length;i++){
            if(nums[i]<0){
                res[neg]=nums[i];neg+=2;
            }
            else{
                res[pos]=nums[i];pos+=2;
            }
        }
        return res;
    }
}