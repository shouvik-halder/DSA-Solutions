public class Solution {
    public bool SearchMatrix(int[][] matrix, int target) {
        int ROWS = matrix.Length;
        int COLS = matrix[0].Length;
        if (matrix.Length == 0 || matrix[0].Length == 0) return false;
        int top =0, bot =ROWS-1;
        int row=0;

        while(top<=bot){
            row = top + (bot-top)/2;

            if(target>matrix[row][COLS-1]){
                top = row+1;
            }
            else if (target<matrix[row][0]){
                bot = row-1;
            }
            else {
                break;
            }
        }

        if(top>bot){
            return false;
        }

        int l=0, r = COLS-1;
        while(l<=r){
            int m = l + (r-l)/2;
            if(target>matrix[row][m]){
                l=m+1;
            }
            else if(target<matrix[row][m]){
                r=m-1;
            }
            else {
                return true;
            }
        }

        return false;

    }
}
