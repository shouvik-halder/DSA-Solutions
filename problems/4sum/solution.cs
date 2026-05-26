public class Solution {
    IList<IList<int>> res;
    List<int> quad;

    public IList<IList<int>> FourSum(int[] nums, int target) {
        Array.Sort(nums);
        res = new List<IList<int>>();
        quad = new List<int>();
        KSum(nums, 4, 0, (long)target);
        return res;
    }

    public void KSum(int[] nums, int k, int start, long target) {
        if (k == 2) {
            int l = start, r = nums.Length - 1;
            while (l < r) {
                long sum = (long)nums[l] + nums[r];
                if (sum > target) r--;
                else if (sum < target) l++;
                else {
                    var newQuad = new List<int>(quad);
                    newQuad.Add(nums[l]);
                    newQuad.Add(nums[r]);
                    res.Add(newQuad);
                    l++; r--;
                    while (l < r && nums[l] == nums[l - 1]) l++;
                    while (l < r && nums[r] == nums[r + 1]) r--;
                }
            }
            return;
        }

        for (int i = start; i < nums.Length - k + 1; i++) {
            if (i > start && nums[i] == nums[i - 1]) continue; // skip duplicates
            quad.Add(nums[i]);
            KSum(nums, k - 1, i + 1, target - nums[i]);
            quad.RemoveAt(quad.Count - 1);
        }
    }
}
