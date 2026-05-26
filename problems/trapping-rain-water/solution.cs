public class Solution {
    public int Trap(int[] heights) {
        int total = 0, lmax = 0, rmax = 0, l = 0;
        int r = heights.Length-1;

        while(l<r){
            if(heights[l]<heights[r]){
                if(lmax>heights[l]) total+=lmax-heights[l];
                else lmax = heights[l];
                l+=1;
            }
            else{
                if(rmax>heights[r]) total+=rmax-heights[r];
                else rmax = heights[r];
                r-=1;
            }
        }

        return total;
    }
}