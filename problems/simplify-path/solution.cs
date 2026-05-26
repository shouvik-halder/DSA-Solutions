public class Solution {
    public string SimplifyPath(string path) {
        Stack<string> stack = new Stack<string>();
        string cur = "";
        foreach (char ch in path+"/"){
            if(ch=='/'){
                if(cur==".."){
                    if(stack.Count>0) stack.Pop();

                }
                else if(cur!="" && cur!="."){
                    stack.Push(cur);
                }
                cur ="";
            }
            else{
                cur+=ch;
            }
        }

        var result = new List<string>(stack);
        result.Reverse();
        return "/" + string.Join("/", result);
    }
}