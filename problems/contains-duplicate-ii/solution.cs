public class Solution {
    public bool ContainsNearbyDuplicate(int[] nums, int k) {
        Dictionary<int, int> lastSeen = new Dictionary<int, int>();
        for(int i=0;i<nums.Length;i++){
            if(lastSeen.ContainsKey(nums[i])){
                if(i-lastSeen[nums[i]]<=k)return true;
                else lastSeen[nums[i]]=i;
            }
            else lastSeen[nums[i]]=i;
        }
        return false;
    }
}