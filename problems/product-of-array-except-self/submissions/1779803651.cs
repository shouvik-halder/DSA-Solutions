public class Solution {
    public int[] ProductExceptSelf(int[] nums) {

    //     int n = nums.Length;

    //     if (n == 0)
    //         return new int[0];

    //     int[] premul = new int[n];
    //     int[] postmul = new int[n];

    //     premul[0] = 1;
    //     postmul[n - 1] = 1;

    //     for (int i = 1; i < n; i++) {
    //         premul[i] = premul[i - 1] * nums[i - 1];
    //     }

    //     for (int i = n - 2; i >= 0; i--) {
    //         postmul[i] = postmul[i + 1] * nums[i + 1];
    //     }

    //     int[] res = new int[n];

    //     for (int i = 0; i < n; i++) {
    //         res[i] = premul[i] * postmul[i];
    //     }

    //     return res;
    // }

    int suffix = 1;
    int n = nums.Length;
    int[] res = new int[n];
    res[0]=1;
    for(int i = 1; i<n;i++){
        res[i] = res[i-1]*nums[i-1];
    }
    for(int i=n-1;i>=0;i--){
        res[i]*=suffix;
        suffix*=nums[i];
    }
    return res;
}
}