public class Solution {
    public void Rotate(int[] nums, int k) {
        int n = nums.Length;
        if(n<=1) return;
        k%=n;

        Array.Reverse(nums,0,n-k);
        Array.Reverse(nums,n-k,k);
        Array.Reverse(nums, 0, n);
    }
}