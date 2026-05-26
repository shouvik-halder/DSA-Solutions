public class Solution {
    public bool IsValid(string s) {
        Dictionary<char, char> data = new Dictionary<char, char>{
            {')', '('},
            {']', '['},
            {'}', '{'}
        };

        Stack<char> stack = new Stack<char>();

        foreach(char ch in s){
            if(data.ContainsKey(ch)){
                if(stack.Count>0 && stack.Peek()==data[ch]){
                    stack.Pop();
                }
                else{
                    return false;
                }
            }
            else{
                stack.Push(ch);
            }
        }

        return stack.Count == 0;
    }
}