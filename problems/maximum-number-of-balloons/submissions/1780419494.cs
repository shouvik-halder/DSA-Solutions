public class Solution {
    public int MaxNumberOfBalloons(string text) {
        Dictionary<char, int> textCount = new Dictionary<char, int>();
        foreach(char ch in text){
            textCount[ch] = textCount.GetValueOrDefault(ch,0)+1;
        }
        Dictionary<char, int> targetCount = new Dictionary<char, int>();
        foreach(char ch in "balloon"){
            targetCount[ch]=targetCount.GetValueOrDefault(ch,0)+1;
        }
    int result = int.MaxValue;;
        foreach(var entry in targetCount){
            result = Math.Min(result, (textCount.GetValueOrDefault(entry.Key,0))/entry.Value);
        }
        return result;
    }
}