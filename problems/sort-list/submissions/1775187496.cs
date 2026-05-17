/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     public int val;
 *     public ListNode next;
 *     public ListNode(int val=0, ListNode next=null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
public class Solution {
    public ListNode SortList(ListNode head) {
        if(head==null || head.next==null) return head;
        return MergeSort(head);
    }

    ListNode MergeSort(ListNode head){
        if(head==null || head.next==null) return head;

        ListNode middle = FindMiddle(head);
        ListNode leftHead = head, rightHead = middle.next;
        middle.next = null;
        leftHead = MergeSort(leftHead);
        rightHead = MergeSort(rightHead);
        return Merge(leftHead, rightHead);
    }

    ListNode FindMiddle(ListNode head){
        ListNode slow = head, fast = head.next;
        while(fast!=null && fast.next!=null){
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    ListNode Merge(ListNode lefthead, ListNode righthead){
        ListNode dummy = new ListNode(-1);
        ListNode temp1 = lefthead, temp2 = righthead, head = dummy;
        while(temp1!=null && temp2!=null){
            if(temp1.val<=temp2.val){
                head.next = temp1;
                temp1 = temp1.next;
            }
            else{
                head.next = temp2;
                temp2 = temp2.next;
            }
            head = head.next;
        }
        head.next = temp1==null?temp2:temp1;
        return dummy.next;
    }
}