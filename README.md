# Hash-Map-Implementation
This repository contains my implementations of two Hash Map variants developed for Oregon State University’s CS261 (Data Structures) course.
The goal of this project was to build core data structures from scratch and reason about correctness, performance, and edge cases such as resizing, and collisions.

## Features

1. Hash Map – Separate Chaining
Uses a dynamic array of singly linked lists for collision handling
Supports:
- Insertion (put)
- Lookup (get, contains_key)
- Removal (remove)
- Resizing with rehashing
= load factor tracking
= Resizing maintains a valid post-resize load factor and preserves all key–value pairs

2. Hash Map – Open Addressing (Quadratic Probing)
Uses a dynamic array and quadratic probing for collision resolution
Supports:
- Tombstones for safe deletion.
- Rehashing during resize.
= Iterator support over active entries.
= Automatically resizes when the load factor becomes too high.

## Concepts Demonstrated
- Hash table design and collision resolution strategies.
- Dynamic resizing and rehashing.
- Load factor invariants.
- Quadratic probing and tombstone handling.

## Testing (Provided by Proffesor)
Each file includes a test section that exercises:
- insertion, deletion, and lookup
- resizing behavior
- load factor constraints
- correct preservation of key–value pairs after rehashing

