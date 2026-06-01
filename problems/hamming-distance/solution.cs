public class Solution {
    public int HammingDistance(int x, int y) {
        int res = 0;
        int xor = x^y;
        while(xor!=0){
            res+=xor&1;
            xor>>=1;
        }

        return res;
    }
}