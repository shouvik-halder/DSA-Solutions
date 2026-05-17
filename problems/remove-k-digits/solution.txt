public class Solution {
    public string RemoveKdigits(string num, int k) {
        if(k>=num.Length) return "0";
        int n = num.Length; Stack<char> st = new Stack<char>();

        for(int i=0;i<n;i++){
            while(k>0 && st.Count!=0 && st.Peek()>num[i]){
                st.Pop();k-=1;
            }
            st.Push(num[i]);
        }

        while(k>0){
            st.Pop();k-=1;
        }

        var result = new string(st.Reverse().ToArray());
        result = result.TrimStart('0');

        return result == ""?"0":result;
        
    }
}