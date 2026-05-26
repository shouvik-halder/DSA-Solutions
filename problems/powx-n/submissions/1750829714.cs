public class Solution {
    public double MyPow(double x, int n) {
        if(n<0){
            x=1/x;
            return PowHelper(x, -(long)n);
        }
        return PowHelper(x, (long)n);
    }

    public double PowHelper(double x, long n)
    {
        if(n==0){
            return 1;
        }
        if(n%2==0){
            return PowHelper(x*x,(long)n/2);
        }
        else{
            return x* PowHelper(x,n-1);
        }
    }
}