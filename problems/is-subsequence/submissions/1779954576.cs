public class Solution {
    public bool IsSubsequence(string s, string t) {
        int lenS = s.Length;
        int lenT = t.Length;
        int indS = 0, indT = 0;
        while(indT<lenT && indS<lenS){
            if(s[indS]==t[indT]){
                indS++;
            }
            indT++;
        }
        return indS == lenS;
}
}