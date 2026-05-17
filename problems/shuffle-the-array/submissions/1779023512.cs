public class Solution {
    public int[] Shuffle(int[] nums, int n) {
        int maxVal = 1001;
        for(int i = n-1;i>=0;i--){
            nums[2*i+1] += (nums[n+i]%maxVal)*maxVal;
            nums[2*i]+=(nums[i]%maxVal)*maxVal;
        }
        
        for(int i=0;i<2*n;i++){
            nums[i]/=maxVal;
        }
        return nums;
    }
}