public class Solution {
    public int CarFleet(int target, int[] position, int[] speed) {
        int n = position.Length;
        int[][] pair = new int[n][];
        
        for (int i = 0; i < n; i++) {
            pair[i] = new int[] { position[i], speed[i] };
        }

        Array.Sort(pair, (a, b) => b[0].CompareTo(a[0]));

        // Stack<double> timeTaken = new Stack<double>();
        int fleet=0;
        double lastTime = 0.0;

        foreach (var car in pair) {
            double time = (double)(target - car[0]) / car[1];
            if (time > lastTime) {
                // timeTaken.Push(time);
                lastTime = time; ++fleet;
            }
        }

        return fleet;
    }
}