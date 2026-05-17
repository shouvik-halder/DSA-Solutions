public class Solution {
    public int MyAtoi(string s) {
        int i =0, isSigned=1, n=s.Length; long result =0;
        
        while(i<n && s[i]==' ') i++;

        if(i<n && (s[i]=='-' || s[i]=='+')){
            isSigned = s[i]=='-'?-1:1;
            i++;
        }
        while(i<n && s[i]>='0'&& s[i]<='9'){
            result = result*10 + (s[i]-'0');
            if(isSigned ==1 && result>int.MaxValue){
                return int.MaxValue;
            }
            else if(isSigned==-1 && -result<int.MinValue){
                return  int.MinValue;
            }

            i++;
        }
            return (int)(isSigned*result);
        }
    
}