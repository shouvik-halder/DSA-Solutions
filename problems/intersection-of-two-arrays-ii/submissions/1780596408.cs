public class Solution {
    public int[] Intersect(int[] nums1, int[] nums2) {
        Dictionary <int, int> count = new Dictionary<int,int>();
        for(int j = 0;j<nums1.Length;j++){
            if(count.ContainsKey(nums1[j])) count[nums1[j]]++;
            else count[nums1[j]]=1;
        }
        List<int> res = new List<int>();
        foreach(int num in nums2){
            if(count.ContainsKey(num)) {
                res.Add(num);count[num]--;
                if(count[num]==0) count.Remove(num);
            }
        }
        return res.ToArray();
    }
}