public class Solution {
    public int SingleNonDuplicate(int[] nums) {
        int n = nums.Length, high = n-1, low = 0;
        while(low<high){
            int mid = (low+high)/2;
            if(mid%2==0){
                if(nums[mid]==nums[mid+1]){
                    low = mid+2;
                }
                else{
                    high = mid;
                }
            }
            else{
                if(nums[mid]==nums[mid-1]){
                    low = mid+1;
                }
                else{
                    high = mid-1;
                }
            }
        }
        return nums[low];
    }
}