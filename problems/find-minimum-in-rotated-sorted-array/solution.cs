public class Solution {
    public int FindMin(int[] nums) {
        int n = nums.Length, high = n - 1, low = 0, ans = int.MaxValue;
        while(low<=high){
            int mid = (low+high)/2;
            if(nums[low]<=nums[mid]){
                ans = Math.Min(ans, nums[low]);
                low = mid+1;
            }
            else{
                ans = Math.Min(ans, nums[mid]);
                high = mid-1;
            }
    }
    return ans;
}
}