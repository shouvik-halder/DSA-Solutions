public class Solution {
    public void SortColors(int[] nums) {
        int low =0, mid=0, high = nums.Length-1;
        while(mid<=high){
            if(nums[mid]==0){
                int tmp = nums[mid];
                nums[mid]= nums[low];
                nums[low]=tmp;
                low++;mid++;
            }
            else if(nums[mid]==2){
                int tmp = nums[mid];
                nums[mid]= nums[high];
                nums[high]=tmp;
                high--;
            }
            else{
                mid++;
            }
        }
    }
}