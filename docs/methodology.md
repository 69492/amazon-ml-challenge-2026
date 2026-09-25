## Blocking

We evaluated multiple blocking strategies to reduce the search space
for entity matching.

### Blocking strategies tested

1. Country + exact normalized business name
2. Country + first meaningful business-name token
3. Country + first meaningful address token
4. Country + first four characters of business name

### Results

| Strategy | Mean Candidate Recall |
|---|---:|
| Exact normalized name | 24.63% |
| Name token | 73.30% |
| Address token | 59.53% |
| Name prefix-4 | 76.05% |
| Combined first three | 84.31% |

The first three strategies provide a useful baseline while keeping
candidate generation more selective. Prefix blocking produces very
large candidate groups and therefore is not used as the primary
blocking strategy.

Blocking is designed to prioritize candidate recall because a
true match removed during blocking cannot be recovered by the
downstream matching model.