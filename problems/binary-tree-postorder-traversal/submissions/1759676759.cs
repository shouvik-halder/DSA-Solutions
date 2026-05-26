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
// public class Solution {
//         private IList<int> tree;
//     public IList<int> PostorderTraversal(TreeNode root) {
//         tree = new List<int>();
//         MorrisTraverse(root);
//         return tree;
//     }

//     public void MorrisTraverse(TreeNode root){
//         TreeNode curr = root;
//         while(curr!=null){
//             if(curr.right==null){
//                 tree.Add(curr.val);
//                 curr = curr.left;
//             }
//             else{
//                 TreeNode prev = curr.right;
//                 while(prev.left!=null && prev.left!=curr){
//                     prev = prev.left;
//                 }

//                 if(prev.left == null){
//                     tree.Add(curr.val);
//                     prev.left = curr;
//                     curr = curr.right;
//                 }
//                 else{
//                     prev.left = null;
//                     curr = curr.left;
//                 }
//             }
//         }

//         tree = tree.Reverse().ToList();
//     }
// }

public class Solution {
    public IList<int> PostorderTraversal(TreeNode root) {
        return travel(root, new List<int>());
    }
    public IList<int> travel(TreeNode root, IList<int> list){
        if(root == null) return list;
        travel(root.left, list);
        travel(root.right, list);
        list.Add(root.val);
        return list;
    }
}