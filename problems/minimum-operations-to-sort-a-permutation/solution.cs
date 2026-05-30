public class Solution {
    public int MinOperations(int[] nums) {
        int isInverted = 0;
        int asc =1, desc =1;int n = nums.Length;
        for(int i = 1;i<n;i++){
            if(nums[i]==((nums[i-1]+1)%n)) asc++;
            else if(nums[i-1]==(nums[i]+1)%n) desc++;
        }
        int x = nums[0];
        if(asc == n && x==0) return 0;
        else if(asc == n) return Math.Min(n-x, x+2);
        else if( desc == n) return 1+Math.Min(n-nums[n-1], nums[n-1]);
        else return -1;
    }
}