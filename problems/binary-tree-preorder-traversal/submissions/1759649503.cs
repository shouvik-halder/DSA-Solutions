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
    private IList<int> tree;
    public IList<int> PreorderTraversal(TreeNode root) {
        tree = new List<int>();
        MorrisTraverse(root);
        return tree;
    }

    public void MorrisTraverse(TreeNode root){
        TreeNode curr = root;

        while(curr!=null){
            if(curr.left == null){
                tree.Add(curr.val);
                curr = curr.right;
            }
            else{
                TreeNode prev = curr.left;
                while(prev.right!=null && prev.right!=curr){
                    prev = prev.right;
                }

                if(prev.right==null){
                    prev.right = curr;
                    tree.Add(curr.val);
                    curr = curr.left;
                }
                else{
                    prev.right = null;
                    curr = curr.right;

                }
            }
        }
    }
}