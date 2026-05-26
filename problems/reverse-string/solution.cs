public class Solution {
    public void ReverseString(char[] s) {
        int n = s.Length;
        int l=0,r=n-1;
        while(l<r){
            char tem = s[l];
            s[l]=s[r];
            s[r]=tem;
            l++;
            r--;
        }
    }
}