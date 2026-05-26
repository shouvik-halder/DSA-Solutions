public class Solution {
    public int[] SearchRange(int[] nums, int target) {
        int low=0,high=nums.Length-1, first=-1,last=-1;
        first = FirstOccurrence(nums, low,high,target);
        if(first==-1)return [-1,-1];
        last = LastOccurrence(nums, low,high,target);
        return [first,last];
}

    private int FirstOccurrence(int[] arr, int low, int high, int target){
        int ans=-1;
        while(low<=high){
            int mid = low+(high-low)/2;
            if(arr[mid]==target){
                ans = mid;high=mid-1;
            }
            else if(arr[mid]<target)
            {
                low=mid+1;
            }
            else{
                high=mid-1;
            }
        }
        return ans;
    }
    private int LastOccurrence(int[] arr, int low, int high, int target){
        int ans=-1;
        while(low<=high){
            int mid = low+(high-low)/2;
            if(arr[mid]==target){
                ans = mid;low=mid+1;
            }
            else if(arr[mid]<target)
            {
                low=mid+1;
            }
            else{
                high=mid-1;
            }
        }
        return ans;
    }
}

