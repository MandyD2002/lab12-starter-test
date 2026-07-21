## chunk

Split items into consecutive lists of at most size elements.

### Parameters

- `items` (`Iterable[_T]`): The input sequence of items to split.
- `size` (`int`): The maximum number of elements per chunk. Must be positive.

### Returns

- `list[list[_T]]`: A list of lists, where each sublist contains up to `size` elements from `items`.

### Example

```python
from collection_helpers import chunk

data = [1, 2, 3, 4, 5, 6, 7]
result = chunk(data, 3)
print(result)  # Output: [[1, 2, 3], [4, 5, 6], [7]]
```

---

## unique

Return items with duplicates removed, preserving first-seen order.

### Parameters

- `items` (`Iterable[_T]`): The input sequence of items, possibly containing duplicates.

### Returns

- `list[_T]`: A list of items with duplicates removed, preserving the order of their first occurrence.

### Example

```python
from collection_helpers import unique

data = [1, 2, 2, 3, 1, 4]
result = unique(data)
print(result)  # Output: [1, 2, 3, 4]
```

---

## group_by

Group items into a dict keyed by key(item), preserving insertion order.

### Parameters

- `items` (`Iterable[_T]`): The input sequence of items to group.
- `key` (`Callable[[_T], _K]`): A function that computes a key for each item.

### Returns

- `dict[_K, list[_T]]`: A dictionary mapping each key to a list of items with that key.

### Example

```python
from collection_helpers import group_by

data = ['apple', 'banana', 'apricot', 'blueberry']
result = group_by(data, key=lambda x: x[0])
print(result)  # Output: {'a': ['apple', 'apricot'], 'b': ['banana', 'blueberry']}
```