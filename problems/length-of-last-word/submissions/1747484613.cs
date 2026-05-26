public class Solution {
    public int LengthOfLastWord(string s) {
        var sarr = s.Trim().Split(' ');
        return sarr[sarr.Length-1].Length;
    }
}