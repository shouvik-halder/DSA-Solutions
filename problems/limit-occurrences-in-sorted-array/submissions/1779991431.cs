public class Solution {
    public int[] LimitOccurrences(int[] nums, int k) {
        if (nums.Length == 0 || k == 0)
            return new int[0];

        List<int> res = new List<int>();

        int count = 1;
        res.Add(nums[0]);

        for (int i = 1; i < nums.Length; i++) {

            if (nums[i] == nums[i - 1]) {
                count++;
            } else {
                count = 1;
            }

            if (count <= k) {
                res.Add(nums[i]);
            }
        }

        return res.ToArray();
    }
}