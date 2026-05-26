public class Solution {
    public int MissingNumber(int[] nums) {
        int n = nums.Length;
        // brute
    //     for(int i=0;i<=n;i++)
    //     {
    //         bool flag=false;
    //         for(int j=0;j<n;j++)
    //         {
    //             if(nums[j]==i)
    //                 flag =true; break;
    //         }

    //         if(!flag)
    //             return i;
    //     }
    //     return 0;
    // }

    // better
    // int[] arr = new int[n+1];
    // Array.Fill(arr,-1);
    // for(int i=0;i<n;i++)
    // {
    //     arr[nums[i]]=1;
    // }

    // for(int i=0;i<=n;i++){
    //     if(arr[i]==-1)
    //         return i;
    // }

    // return 0;

    // optimum
    int sum = n*(n+1)/2;
    int sumarr =0;
    for(int i=0;i<n;i++){
        sumarr+=nums[i];
    }
    return sum-sumarr;
}}