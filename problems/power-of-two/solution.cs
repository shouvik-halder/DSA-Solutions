public class Solution {
    public bool IsPowerOfTwo(int n) {
        // brute
        // int count =0;
        // while(n!=0){
        //     count+=(n&1);
        //     n>>=1;
        // }

        // return count ==1;
        return n > 0 && (n & (n - 1)) == 0;
    }
}