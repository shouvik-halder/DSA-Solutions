public class Solution {
    public string LongestCommonPrefix(string[] strs) {
        if (strs==null || strs.Length ==0) return "";
        int strsLen =  strs.Length;
        int strLen = strs[0].Length;

        for(int i = 0; i< strLen;i++){
            char curr = strs[0][i];
            for(int j = 0; j<strsLen;j++){
                if(i>=strs[j].Length || strs[j][i]!=curr) return strs[0].Substring(0, i);
            }
        }
        return strs[0];
    }
}