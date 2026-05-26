public class Solution {
    public int[] ProductExceptSelf(int[] nums) {
        // int[] premul = new int[nums.Length];
        // int[] postmul = new int[nums.Length];
        // int[] res = new int[nums.Length];
        // premul[0]=1;
        // postmul[nums.Length-1]=1;
        // for(int i = 1;i<nums.Length;i++){
        //     premul[i]= premul[i-1]*nums[i-1];
        // }
        // for(int i = nums.Length-2;i>=0;i--){
        //     postmul[i]= postmul[i+1]*nums[i+1];
        // }

        // for(int i=0;i<nums.Length;i++){
        //     res[i]=premul[i]*postmul[i];
        // }
        // return res;

        int[] res = new int[nums.Length];
        Array.Fill(res,1);
        int prefix =1, suffix =1;
        for(int i=0;i<nums.Length;i++){
            res[i]=prefix;
            prefix = nums[i]* prefix;
        }

        for(int i=nums.Length-1;i>=0;i--){
            res[i]=res[i]*suffix;
            suffix = nums[i]* suffix;
        }

        return res;
    }
}