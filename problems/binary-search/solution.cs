public class Solution {
    public int Search(int[] nums, int target) {
        int low = 0,n = nums.Length,  high = n-1;

        while(low<=high){
            int mid = (low+high)/2;
            if(nums[mid]>target){
                high=mid-1;
            }
            else if(nums[mid]<target){
                low=mid+1;
            }
            else{
                return mid;
            }
        }
        return -1;
    }
}