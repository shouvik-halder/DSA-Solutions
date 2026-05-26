public class Solution {
    public int[] AsteroidCollision(int[] asteroids) {
        Stack<int> st = new Stack<int>();

        foreach (var item in asteroids) {
            int curr = item;

            while (st.Count != 0 && st.Peek() > 0 && curr < 0) {
                if (st.Peek() + curr < 0) {
                    st.Pop();
                }
                else if (st.Peek() + curr == 0) {
                    st.Pop();
                    curr = 0;
                    break;
                }
                else {
                    curr = 0;
                    break;
                }
            }

            if (curr != 0) {
                st.Push(curr);
            }
        }

        return st.Reverse().ToArray();
    }
}