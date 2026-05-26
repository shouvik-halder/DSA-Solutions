public class Solution {
    public int LongestConsecutive(int[] nums) {
        HashSet<int> data = new HashSet<int>(nums);
        int n= nums.Length, longest = 1, cnt =1;
        if(n==0){
            return 0;
        }
        // for(int i=0;i<n;i++){
        //     data.Add(nums[i]);
        // }
        foreach(int num in data){
            if(!data.Contains(num-1)){
                cnt =1;
                while(data.Contains(num+cnt)){
                    ++cnt; 
                }
                longest = Math.Max(cnt, longest);
            }
        }
        return longest;
    }
}