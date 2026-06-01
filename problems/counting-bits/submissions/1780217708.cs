public class Solution {
    public int[] CountBits(int n) {
        if(n==0) return new int[]{0};
        int[] res = new int[n+1];
        // brute
        // res[0]=0;
        // for(int i=1;i<=n;i++){
        //     int x =i;
        //     while(x!=0){
        //         res[i]+=x&1;
        //         x=x>>1;
        //     }
        // }


        for(int i=1;i<=n;i++){
            res[i]=res[i>>1]+(i&1);
        }
        return res;


    }
}