public class Solution {
    public int MinEatingSpeed(int[] piles, int h) {
        int l=1, r = piles.Max(), res = r;

        while(l<=r){
            int m = l+(r-l)/2; double totalTime = 0;
            foreach(var pile in piles){
                totalTime+= Math.Ceiling((double)pile/m);
            }

            if(totalTime<=h){
                res = m;
                r=m-1;
            }
            else{
                l=m+1;
            }
        }

        return res;
    }
}
