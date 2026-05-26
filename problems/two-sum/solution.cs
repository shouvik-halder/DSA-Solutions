public class Solution {
    public int[] TwoSum(int[] nums, int target) {
        Dictionary<int, int> sumPair = new Dictionary<int, int>();
        int i=0;
        int n= nums.Length;
        while(i<n)
        {
            if(sumPair.ContainsKey(nums[i]))
            {
                return [sumPair[nums[i]],i];
            }
            if(!sumPair.ContainsKey(target-nums[i])){
                sumPair.Add(target-nums[i],i);
            }
            i++;
        }
        return [0,0];
    }
}