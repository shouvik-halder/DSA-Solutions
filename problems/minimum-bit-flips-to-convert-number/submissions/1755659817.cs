public class Solution {
    public int MinBitFlips(int start, int goal) {
        int flipReq = start^goal, cnt=0;
        while(flipReq!=0){
            flipReq=flipReq&(flipReq-1);
            ++cnt;
        }
        return cnt;
    }
}