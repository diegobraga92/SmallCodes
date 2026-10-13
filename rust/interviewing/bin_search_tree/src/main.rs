/*
Generic Binary Search Tree
--------------------------------------------------------
- Insert
- Contains
- Inorder traversal iterator

Senior signal:
- Ownership modeling
- Option<Box<Node<T>>>
- Generics with Ord
*/

use std::cmp::Ordering;

struct Node<T: Ord> {
    value: T,
    left: Option<Box<Node<T>>>,
    right: Option<Box<Node<T>>>,
}

struct BinSearchTree<T: Ord> {
    root: Option<Box<Node<T>>>,
}

impl<T: Ord> BinSearchTree<T> {
    fn new() -> Self {
        Self { root: None }
    }

    fn insert(&mut self, v: T) {
        let mut curr = &mut self.root;

        while let Some(node) = curr {
            match v.cmp(&node.value) {
                Ordering::Less => curr = &mut node.left,
                Ordering::Greater => curr = &mut node.right,
                Ordering::Equal => return,
            }
        }

        *curr = Some(Box::new(Node {
            value: v,
            left: None,
            right: None,
        }));
    }

    fn contains(&self, v: &T) -> bool {
        let mut curr = self.root.as_deref();

        while let Some(node) = curr {
            match v.cmp(&node.value) {
                Ordering::Less => curr = node.left.as_deref(),
                Ordering::Greater => curr = node.right.as_deref(),
                Ordering::Equal => return true,
            }
        }

        false
    }

    fn inorder(&self) -> Vec<&T> {
        fn traverse<'a, T: Ord>(node: &'a Option<Box<Node<T>>>, out: &mut Vec<&'a T>) {
            if let Some(n) = node {
                traverse(&n.left, out);
                out.push(&n.value);
                traverse(&n.right, out);
            }
        }

        let mut res = Vec::new();
        traverse(&self.root, &mut res);
        res
    }
}

fn main() {
    let mut bst = BinSearchTree::new();

    bst.insert(5);
    bst.insert(3);
    bst.insert(7);
    bst.insert(1);
    bst.insert(3); // duplicate

    assert!(bst.contains(&5));
    assert!(bst.contains(&1));
    assert!(!bst.contains(&9));

    let values: Vec<i32> = bst.inorder().into_iter().copied().collect();
    assert_eq!(values, vec![1, 3, 5, 7]);

    println!("All tests passed.");
}
