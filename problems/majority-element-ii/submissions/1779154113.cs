public class Solution {
    public IList<int> MajorityElement(int[] nums) {
        if(nums.Length == 1) return new List<int>{nums[0]};
        int count1 = 0, count2 = 0, res1 = 0, res2=0;
        foreach(int num in nums){
            if(num==res1) count1++;
            else if(num==res2) count2++;
            else if(count1 ==0){
                res1 = num;
                count1++;
            }
            else if(count2==0){
                res2 = num;
                count2++;
            }
            else{
                count1--;
                count2--;
            }
        }

        count1=0;count2=0;
        foreach(int num in nums){
            if(num == res1)count1++;
            if(res1!=res2 && num == res2)count2++;
        }
        var res = new List<int>();
        if(count1>nums.Length/3) res.Add(res1);
        if(count2>nums.Length/3) res.Add(res2);

        return res;
    }
}