public class Solution {
    public int NumIdenticalPairs(int[] nums) {
        int[] freq = new int[101];
        int count = 0;
        foreach(int num in nums){
            count+=freq[num];
            freq[num]++;
        }
        return count;
    }
}