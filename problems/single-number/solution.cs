public class Solution {
    public int SingleNumber(int[] nums) {
        // better
        // Dictionary<int,int> num = new Dictionary<int,int>();
        // for(int i=0;i<nums.Length;i++){
        //     if(num.ContainsKey(nums[i])){
        //     num[nums[i]]++;
        //     }
        //     else{
        //         num.Add(nums[i],1);
        //     }
        // }

        // foreach(var item in num){
        //     if(item.Value == 1){
        //         return item.Key;
        //     }
        // }

        // best
        int xor=0;
        for(int i=0;i<nums.Length;i++){
            xor = xor ^ nums[i];
        }
        return xor;
    // return -1;
    }
}