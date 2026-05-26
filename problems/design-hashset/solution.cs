public class ListNode {
    public int Key;
    public ListNode Next;

    public ListNode(int key) {
        Key = key;
        Next = null;
    }
}

public class MyHashSet {
    private ListNode[] set;

    public MyHashSet() {
        set = new ListNode[10000];
        for (int i = 0; i < set.Length; i++) {
            set[i] = new ListNode(0); // Dummy head
        }
    }

    public void Add(int key) {
        ListNode cur = set[key % set.Length];
        while (cur.Next != null) {
            if (cur.Next.Key == key) return;
            cur = cur.Next;
        }
        cur.Next = new ListNode(key);
    }

    public void Remove(int key) {
        ListNode cur = set[key % set.Length];
        while (cur.Next != null) {
            if (cur.Next.Key == key) {
                cur.Next = cur.Next.Next;
                return;
            }
            cur = cur.Next;
        }
    }

    public bool Contains(int key) {
        ListNode cur = set[key % set.Length];
        while (cur.Next != null) {
            if (cur.Next.Key == key) return true;
            cur = cur.Next;
        }
        return false;
    }
}