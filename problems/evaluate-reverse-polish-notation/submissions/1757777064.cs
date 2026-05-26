public class Solution {
    public int EvalRPN(string[] tokens) {
       Stack<int> stack = new Stack<int>();

        foreach(var item in tokens){
            if(item == "+"){
                var a = stack.Pop();
                var b = stack.Pop();
                stack.Push(b+a);
            }
            else if(item == "-"){
                var a = stack.Pop();
                var b = stack.Pop();
                stack.Push(b-a);
            }
            else if(item == "*"){
                var a = stack.Pop();
                var b = stack.Pop();
                stack.Push(b*a);
            }
            else if(item == "/"){
                var a = stack.Pop();
                var b = stack.Pop();
                stack.Push(b/a);
            }
            else{
                stack.Push(int.Parse(item));
            }
        }
        return stack.Peek(); 
    }
}