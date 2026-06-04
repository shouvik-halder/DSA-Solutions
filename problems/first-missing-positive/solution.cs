public class Solution {
    public int FirstMissingPositive(int[] nums) {
        bool isPresent1 = false;int n=nums.Length;
        for(int i=0;i<n;i++){
            if(nums[i]==1) isPresent1=true;
            else if(nums[i]<=0||nums[i]>n) nums[i]=1;
        }

        if(!isPresent1)return 1;
        for(int i=0;i<n;i++){
            int idx = Math.Abs(nums[i])-1;
            if(nums[idx]>0) nums[idx]=-nums[idx];
        }

        for(int i=0;i<n;i++){
            if(nums[i]>0) return i+1;
        }

        return n+1;
    }
}