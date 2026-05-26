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
    public IList<int> InorderTraversal(TreeNode root) {
        tree = new List<int>();
        // traverse(root);
        MorrisTraverse(root);
        return tree;
    }

    // public void traverse(TreeNode root){
    //     if (root ==null){
    //         return;
    //     }

    //     traverse(root.left);
    //     tree.Add(root.val);
    //     traverse(root.right);
    // }

    public void MorrisTraverse(TreeNode root){
        TreeNode curr = root;

        while(curr!=null){
            if(curr.left == null)
            {
                tree.Add(curr.val);
                curr = curr.right;
            }
            else
            {
                TreeNode prev = curr.left;
                while(prev.right!=null && prev.right!=curr){
                    prev = prev.right;
                }

                if(prev.right == null){
                    prev.right = curr;
                    curr = curr.left;
                }
                else{
                    prev.right = null;
                    tree.Add(curr.val);
                    curr = curr.right;
                }
            }
        }

    }
}