public class Solution {
    public int ShipWithinDays(int[] weights, int days) {
        int low = weights.Max(),max=weights.Sum();


        while(low<=max){
            int mid=low+(max-low)/2;

            int usedDays=1;
            int currLoad=0;
            foreach(int weight in weights){
                if(currLoad+weight>mid){
                    usedDays++;
                    currLoad=0;
                }
                currLoad+=weight;
            }
            if(usedDays<=days){
                max=mid-1;
            }
            else{
                low=mid+1;
            }
        }
        return low;
    }
}