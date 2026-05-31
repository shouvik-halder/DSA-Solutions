public class Solution {
    public int[] FindErrorNums(int[] nums) {
        // Dictionary<int, int> count = new Dictionary<int, int> ();
        // for(int i = 0;i<nums.Length;i++){
        //     if(count.ContainsKey(nums[i])) count[nums[i]]++;
        //     else count[nums[i]]=1;
        // }
        // int dup = 0, miss = 0;
        // for(int i =1;i<=nums.Length;i++){
        //     int check = count.ContainsKey(i)?count[i]:0;
        //     if(check==2) dup= i;
        //     else if (check == 0 )miss = i;
        // }
        // if(miss == 0)miss = nums.Length;

        // return new int[]{dup, miss};
        
        // optimal
        //  intuition: We will be visiting the nums[pos] where pos is the value of nums[i]-1

        int dup = 0; int miss = 0;
        for(int i=0;i<nums.Length;i++){
            int targetIdx = Math.Abs(nums[i])-1;
            if(nums[targetIdx]<0){
                dup = Math.Abs(nums[i]);
            }
            else{
                nums[targetIdx]= -nums[targetIdx];
                }
        }

        for(int i =0;i<nums.Length;i++){
            if(nums[i]>0) miss = i + 1;
        }

        return new int[]{dup, miss};
    }
}