// public class Solution {
//     public void NextPermutation(int[] nums) {
//         int ind = -1;
//         int n = nums.Length;

//         for (int i = n - 2; i >= 0; i--) {
//             if (nums[i] < nums[i + 1]) {
//                 ind = i;
//                 break;
//             }
//         }

//         if (ind == -1) {
//             Array.Reverse(nums);
//             return; 
//         }

//         for (int i = n - 1; i > ind; i--) {
//             if (nums[i] > nums[ind]) {
//                 int temp = nums[i];
//                 nums[i] = nums[ind];
//                 nums[ind] = temp;
//                 break;
//             }
//         }

//         Array.Reverse(nums, ind + 1, n - ind - 1);
//     }
// }

public class Solution {
    public void NextPermutation(int[] nums) {
        int n = nums.Length; int breakPoint = -1;
        for(int i = n-2;i>=0;i--){
            if(nums[i]<nums[i+1]){
                breakPoint = i;
                break;
            }
        }
        if(breakPoint==-1){
            Array.Reverse(nums);
            return;
        }
        else{
            for(int i = n-1;i>breakPoint; i--){
                if(nums[breakPoint]<nums[i]){
                    (nums[breakPoint], nums[i]) = (nums[i], nums[breakPoint]);
                    break;
                }
            }
            Array.Reverse(nums, breakPoint+1, n-breakPoint-1);
            return;
        }
    }
}