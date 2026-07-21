# Numeric helpers: averages, clamping, and percentage maths

## compute_average

Return the arithmetic mean of values, or 0.0 for an empty sequence.

### Parameters

- `values` (Sequence[float]): The sequence of numeric values to average.

### Returns

- `float`: The arithmetic mean of the values, or 0.0 if the sequence is empty.

### Example

```python
from numeric_helpers import compute_average

numbers = [10.0, 20.0, 30.0]
avg = compute_average(numbers)
print(avg)  # Output: 20.0

empty = []
print(compute_average(empty))  # Output: 0.0
```

---

## clamp

Clamp value into the inclusive range [low, high].

### Parameters

- `value` (float): The value to clamp.
- `low` (float): The lower bound of the range.
- `high` (float): The upper bound of the range.

### Returns

- `float`: The clamped value, guaranteed to be within [low, high].

### Example

```python
from numeric_helpers import clamp

print(clamp(5.0, 1.0, 10.0))   # Output: 5.0
print(clamp(-3.0, 0.0, 100.0)) # Output: 0.0
print(clamp(150.0, 0.0, 100.0))# Output: 100.0

# Raises ValueError if low > high
try:
    clamp(5.0, 10.0, 1.0)
except ValueError as e:
    print(e)  # Output: low must not exceed high
```

---

## percentage

Return part as a percentage of whole, rounded to two decimal places.

Returns 0.0 when whole is zero rather than raising.

### Parameters

- `part` (float): The numerator value.
- `whole` (float): The denominator value.

### Returns

- `float`: The percentage value (rounded to two decimal places), or 0.0 if `whole` is zero.

### Example

```python
from numeric_helpers import percentage

print(percentage(25.0, 100.0))  # Output: 25.0
print(percentage(5.0, 20.0))    # Output: 25.0
print(percentage(1.0, 0.0))     # Output: 0.0
```