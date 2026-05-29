public class Solution {
    public bool RotateString(string s, string goal) {
        int n = s.Length;
        if(s==goal) return true;
        for(int i=1;i<n;i++){
            if(s.Substring(i,n-i)+ s.Substring(0, i) == goal) return true;
        }
        return false;
    }
}