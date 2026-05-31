public class Solution {
    public int[] SingleNumber(int[] nums) {
        int unique = 0;
        foreach(int num in nums){
            unique^=num;
        }

        // now unique has x^y
        // Now we check what is the rightmost bit that is set for unique
        int diffbit = unique & -unique;
        // diffBit stores the location of the bit which is set;
    int x=0;
        foreach(int num in nums){
            if((num & diffbit)!=0){
                x^=num;
            }
        }

        return new int[] {x, x^unique};
    }
}