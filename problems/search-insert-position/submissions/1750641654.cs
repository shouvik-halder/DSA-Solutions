public class Solution {
    public int SearchInsert(int[] nums, int target) {
        int low = 0; int high = nums.Length -1;int ans = nums.Length;
        while (low<=high)
        {
            int mid = (low+high)/2;
            if(nums[mid]>=target){
                ans = mid;
                high = mid-1;
            }
            else {
                low = mid+1;
            }
        }
        return ans;
    }
}