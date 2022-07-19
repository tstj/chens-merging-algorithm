# Optimizing Chen's in-place merging algorithm

- Chen's in-place merging algorithm [1] requires for large input sequences up to ~1.26 * (M+N) comparisons and 3 * (M+N) moves, where M and N are two adjacent input sequences and |M| <= |N|. The merging algorithm is not stable (same elements may change their order).
- We can observe, that the number of comparisons can be reduced to a worst case of ~1.13 * (M+N) by setting the start index of `find-next-X-block` properly, which will eliminate ~ |M| / 4 comparisons.
- We can achieve this optimization, by adding the parameter `y0` to `find-next-X-block` and adding one line in this procedure. After `i = m`, we add the line `if z != x0: i = max(i, y0-2*k)`.
- Additionally, we can observe that the block orders are partly structured and further analysis of the block order may reduce the number of comparisons, by calculating the next block without any comparisons (would result in the optimal worst case M + N - 1 = 1.00 * (M+N) - 1 comparisons) or at least limiting the search space of the possible blocks in `find-next-X-block` (1.07 * (M+N) comparisons seems possible).

[1] Jing-Chao Chen: A simple algorithm for in-place merging. Inf. Process. Lett. 98(1): 34-40 (2006)

