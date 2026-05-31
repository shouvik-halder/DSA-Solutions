public class Solution {
    public int SingleNumber(int[] nums) {
        // brute
        // Dictionary<int, int> count = new Dictionary<int,int>();
        // for(int i =0;i<nums.Length;i++){
        //     if(!count.ContainsKey(nums[i]))count[nums[i]]=1;
        //     else count[nums[i]]++;
        // }

        // foreach(var check in count ){
        //     if(check.Value ==1) return check.Key;
        // }

        // return -1;

        // optimal we count the number of set bits in each bit position
        // if the bits are divisible by 3 then the contibution of that bit position is not contributed by the single value
        // int res = 0;
        // for(int i = 0;i<32;i++){

        //     int bitSum = 0;

        //     foreach(int num in nums){
        //         bitSum+=(num>>i) & 1;
        //     }

        //     if(bitSum%3==1){
        //         res|=(1<<i);
        //     }
        // }

        // return res;


        // best
        // Check the count of bit set all at once;

        int ones = 0;int twos = 0;
        foreach(int num in nums){
            ones = (ones^num) &~twos;
            twos = (twos^num) & ~ones;
        }

        return ones;

    }
}