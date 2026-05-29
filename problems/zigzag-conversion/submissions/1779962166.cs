public class Solution {
    public string Convert(string s, int numRows) {
        if(s.Length==numRows || numRows ==1 || s.Length <=1) return s;

        string[] arr = new string[numRows];

        int direction = 1;int row = 0;
        foreach(char ch in s){
            arr[row] = arr[row]+ch;
            if(row == 0) {direction =1; row++;}
            else if(row == numRows-1) {direction = -1; row --;}
            else row+=direction;
        }
        string res = string.Empty;
        foreach(string rowdata in arr){
            res+=rowdata;
        }
        return res;
    }
}