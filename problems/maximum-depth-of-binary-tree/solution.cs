/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     public int val;
 *     public TreeNode left;
 *     public TreeNode right;
 *     public TreeNode(int val=0, TreeNode left=null, TreeNode right=null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
public class Solution {
     public int MaxDepth(TreeNode root) {
        if(root == null) return 0;
        return 1+ Math.Max(MaxDepth(root.left), MaxDepth(root.right));
        // return Depth(root, 0);
    }

    public int Depth(TreeNode root, int level){
        if(root == null) return level;

        int l = Depth(root.left, level+1);
        int r = Depth(root.right, level+1);
        return Math.Max(l,r);
    }
}