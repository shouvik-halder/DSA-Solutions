public class Solution {
    public int CalPoints(string[] operations) {
        Stack<int> rec = new Stack<int>();
        foreach(var op in operations){
            if(op == "+"){
                var top = rec.Pop();
                int newTop = top+rec.Peek();
                rec.Push(top);
                rec.Push(newTop);
            }
            else if(op == "C"){
                rec.Pop();
            }
            else if(op == "D"){
                rec.Push(2*rec.Peek());
            }
            else{
                rec.Push(int.Parse(op));
            }
        }
        int total = 0;
        foreach( var val in rec){
            total +=val;
        }
        return total;
    }
}