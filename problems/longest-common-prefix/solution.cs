public class Solution {
    public string LongestCommonPrefix(string[] strs) {
        if (strs == null || strs.Length == 0)
        return string.Empty;

        Array.Sort(strs);
        var first = strs[0];
        var last = strs[^1];
        int minLength = Math.Min(first.Length, last.Length);
        int i = 0;

        while(i<minLength && first[i]==last[i]) {
            i++;
        }

        return first.Substring(0,i);
    }
}