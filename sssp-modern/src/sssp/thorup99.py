"""Thorup 1999 hierarchical bucket SSSP for undirected graphs.

This module provides a reference implementation of Thorup's 1999 single-source
shortest path algorithm. For undirected graphs with non-negative integer
weights, the original algorithm achieves an O(m + n) runtime bound using a
hierarchical bucket structure on a word-RAM model.

Python Runtime-Model Caveat:
Python does not provide a strict O(1) word-RAM execution model. Python integers
are arbitrary-precision objects, and bitwise operations do not execute in O(1)
relative to a constant machine word size. The overhead of Python's dynamic
typing, memory allocation, and object references dominates the constant factors.
Therefore, this implementation is provided strictly as a reference to demonstrate
the behavioral and structural correctness of the hierarchical bucket concept. It
does not claim to achieve the theoretical O(m + n) linear-time performance bound
in practice when run in the CPython interpreter.

Hierarchy Structure:
This implementation simplifies the exact component hierarchy into a bitwise
hierarchical bucket queue (similar to a radix heap). Vertices are grouped into
buckets based on the most significant differing bit (MSDB) between their
tentative distance and the current minimum extracted distance. When the minimum
distance advances, buckets are split and redistributed, ensuring only relevant
buckets are scanned.
"""

from __future__ import annotations

import math
from typing import Any

from sssp.graph import Graph, Vertex

Distances = dict[Vertex, Any]


def _msdb(a: int, b: int) -> int:
    """Return the most significant differing bit (1-indexed) between a and b.
    Returns 0 if a == b.
    """
    diff = a ^ b
    if diff == 0:
        return 0
    return diff.bit_length()


def thorup_sssp(graph: Graph, source: Vertex) -> Distances:
    """Return reachable single-source distances using a hierarchical bucket queue.

    Preconditions:
    - `graph` must be undirected.
    - `source` must be a vertex in `graph`.
    - edge weights must be non-negative integers.

    Returns:
    - A dictionary mapping reachable vertices to their integer distances.
    """
    if graph.is_directed:
        raise ValueError("thorup_sssp requires an undirected graph")

    if source not in set(graph.vertices()):
        raise ValueError("source must be a vertex in graph")

    # Validate weights upfront for immediate failure, though typically checked during traversal.
    # To avoid O(E) upfront scan, we'll check during relaxation, but to be safe for isolated tests,
    # let's do a quick type check if there are any edges.
    
    # We maintain distances and a radix heap of tentative distances
    distances: Distances = {source: 0}
    settled: set[Vertex] = set()

    # The buckets: bucket[i] holds vertices where _msdb(dist, last_min) == i
    # The maximum possible distance in Python is unbounded, but bit_length gives us the bucket index.
    # We can just use a dynamic list of lists or dictionary for buckets.
    buckets: dict[int, list[Vertex]] = {}
    buckets[0] = [source]
    
    # Track the current minimum distance extracted
    last_min = 0
    
    # Track the tentative distance for each vertex in the queue
    queue_dist: dict[Vertex, int] = {source: 0}
    
    # Track the number of vertices currently in the queue
    queue_size = 1

    while queue_size > 0:
        # Find the lowest non-empty bucket
        min_bucket_idx = -1
        for i in sorted(buckets.keys()):
            if buckets[i]:
                min_bucket_idx = i
                break
                
        if min_bucket_idx == -1:
            break  # queue is conceptually empty

        # If the lowest non-empty bucket is > 0, we must extract its minimum,
        # update last_min, and redistribute its contents.
        if min_bucket_idx > 0:
            # Find the true minimum in this bucket, ignoring settled vertices
            raw_bucket = buckets[min_bucket_idx]
            buckets[min_bucket_idx] = []
            
            current_bucket = [v for v in raw_bucket if v not in settled]
            queue_size -= (len(raw_bucket) - len(current_bucket))
            
            if not current_bucket:
                continue
            
            new_min = min(queue_dist[v] for v in current_bucket)
            last_min = new_min
            
            # Redistribute
            for v in current_bucket:
                idx = _msdb(queue_dist[v], last_min)
                if idx not in buckets:
                    buckets[idx] = []
                buckets[idx].append(v)
            
            # The minimums are now in bucket 0
            continue
            
        # min_bucket_idx == 0
        # All vertices in bucket 0 have distance == last_min
        current_bucket = buckets[0]
        buckets[0] = []
        queue_size -= len(current_bucket)
        
        for u in current_bucket:
            if u in settled:
                continue
                
            settled.add(u)
            dist_u = queue_dist[u]
            distances[u] = dist_u
            del queue_dist[u]
            
            for edge in graph.neighbors(u):
                w = edge.weight
                if not isinstance(w, int) or isinstance(w, bool):
                    raise ValueError("thorup_sssp requires integer edge weights")
                if w < 0:
                    raise ValueError("thorup_sssp requires non-negative edge weights")
                    
                v = edge.target
                if v in settled:
                    continue
                    
                new_dist = dist_u + w
                old_dist = queue_dist.get(v)
                
                if old_dist is None or new_dist < old_dist:
                    queue_dist[v] = new_dist
                    idx = _msdb(new_dist, last_min)
                    
                    # We just append to the new bucket (lazy deletion). 
                    # We will ignore stale entries when popping.
                    queue_size += 1
                        
                    if idx not in buckets:
                        buckets[idx] = []
                    buckets[idx].append(v)

    # Clean up distances to only return reachable vertices
    # Our algorithm actually sets distances exactly for reachable vertices
    return distances
