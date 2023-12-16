# Algorithms and Data Structures Phase-2: Binary Trees and Binary Search

This repository is part of a series for an Algorithms and Data Structures class, specifically focusing on binary trees and binary search trees (BSTs). The project demonstrates the implementation and application of these fundamental data structures in Python.

## About The Project

The project features the implementation of binary trees and their operations such as insertion, deletion, and traversal. It then extends these concepts to binary search trees, which are a type of binary tree where the tree is ordered, making search operations efficient. Additionally, the project includes a practical application in the form of a health center scheduling system that utilizes BSTs to manage patient appointments effectively.

### Modules

- `binarytree.py`: Contains the implementation of a basic binary tree.
- `binarysearchtree.py`: Extends `binarytree.py` to implement a BST with additional functionalities.
- `fase2.py`: Uses the BST to create a health center scheduling system, handling patient data and appointments.
- `fase2__unitest.py`: Provides a suite of unit tests to ensure the correctness of the implemented data structures and their methods.

## Usage

The modules can be imported and used in your Python projects. For example:

```
from binarysearchtree import BinarySearchTree

# Create a new Binary Search Tree
bst = BinarySearchTree()

# Insert elements
bst.insert(50, "Data1")
bst.insert(30, "Data2")
bst.insert(20, "Data3")

# Print in order
bst.inorder()
```

## Contact

Rosa Reyes: [LinkedIn](https://www.linkedin.com/in/rosaareyesc/)
