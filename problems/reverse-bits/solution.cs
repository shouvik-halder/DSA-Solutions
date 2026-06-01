public class Solution {
    public int ReverseBits(int n) {
        int result = 0;
        for(int i =0;i<32;i++){
            result = result<<1 | (n&1);
            n>>=1;
        }

        return result;
    }
}