public class MinStack {
Stack<int> stack;
    Stack<int>minVal;
    public MinStack() {
        stack = new Stack<int>();
        minVal = new Stack<int>();
    }
    
    public void Push(int val) {
        stack.Push(val);
        val = Math.Min(val, minVal.Count==0? val: minVal.Peek());
        minVal.Push(val);
    }
    
    public void Pop() {
        stack.Pop();
        minVal.Pop();
    }
    
    public int Top() {
        return stack.Peek();
    }
    
    public int GetMin() {
        return minVal.Peek();
    }
}

/**
 * Your MinStack object will be instantiated and called as such:
 * MinStack obj = new MinStack();
 * obj.Push(val);
 * obj.Pop();
 * int param_3 = obj.Top();
 * int param_4 = obj.GetMin();
 */