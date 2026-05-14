# Decision Note: Thorup 1999 Hierarchical Bucket SSSP Runtime Model

## Context
We are adding a reference implementation of Thorup's 1999 single-source shortest path (SSSP) algorithm for undirected graphs with non-negative integer weights. The original algorithm achieves an $O(m + n)$ runtime bound using a hierarchical bucket structure on a word-RAM model, exploiting fast bitwise operations and the properties of undirected graphs.

## Hierarchy Design
The reference implementation will use a simplified hierarchical bucket structure:
1.  **Hierarchy Invariants**: Vertices are grouped into buckets based on the most significant differing bit (MSDB) between their tentative distance and the current minimum distance. 
2.  **Bucket Transitions**: When the current minimum distance advances, buckets containing closer vertices are split and redistributed to lower-level buckets, ensuring we only scan buckets known to contain the next minimum.
3.  **Simplifications**: Instead of the full component hierarchy mapping originally described by Thorup to avoid any sorting, our reference implementation may use an explicit bitwise-trie or tiered bucket array. This simulates the essential property of Thorup's approach (avoiding the heap's $O(\log n)$ overhead per relaxation) by using constant-time (in Python terms) bitwise routing.

## Runtime-Model Caveat
**Python vs. Word-RAM Model**:
Python does not provide a strict word-RAM execution model.
- Python integers are arbitrary-precision objects, not fixed-size machine words. Bitwise operations are not strictly $O(1)$ relative to a constant machine word size.
- The overhead of Python's dynamic typing, memory allocation, and object references dominates the constant factors.
- Therefore, this implementation is provided strictly as a **reference implementation** to demonstrate the behavioral and structural correctness of the hierarchical bucket concept. It **does not claim** to achieve the theoretical $O(m + n)$ linear-time performance bound in practice when run in the CPython interpreter.

This caveat must be clearly documented in the module docstring of the implementation.
