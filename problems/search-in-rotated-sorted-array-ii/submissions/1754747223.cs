public class Solution {
    public bool Search(int[] nums, int target) {
        int n = nums.Length, high = n-1, low = 0;
        while(low <=high){
            int mid = (low+high)/2;
            if(nums[mid] == target)return true;
            else if(nums[low] == nums[mid] && nums[low]==nums[high]){
                ++low; --high ;
            }
            else if(nums[low]<= nums[mid]){
                if(nums[low]<=target && target <= nums[mid]){
                    high = mid-1;
                }
                else{
                    low = mid+1;
                }
            }
            else{
                if(nums[mid]<=target && target <= nums[high]){
                                    low = mid+1;
                                }
                                else{
                                    high = mid-1;
                                }
            }
        }
        return false;
    }
}