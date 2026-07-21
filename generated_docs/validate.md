# API Reference

## is_email

Return True if value looks like a single, well-formed email address.

### Parameters

- `value` (`str`): The string to validate as an email address.

### Returns

- `bool`: True if `value` is a well-formed email address, otherwise False.

### Example

```python
from validators import is_email

print(is_email("user@example.com"))     # True
print(is_email("not-an-email"))         # False
print(is_email("user@domain"))          # False
print(is_email("user@example.com "))    # True
```

---

## is_in_range

Return True if low <= value <= high.

### Parameters

- `value` (`float`): The numeric value to check.
- `low` (`float`): The lower bound of the range (inclusive).
- `high` (`float`): The upper bound of the range (inclusive).

### Returns

- `bool`: True if `value` is within the range `[low, high]`, otherwise False.

### Example

```python
from validators import is_in_range

print(is_in_range(5, 1, 10))    # True
print(is_in_range(0, 1, 10))    # False
print(is_in_range(10, 1, 10))   # True
print(is_in_range(11, 1, 10))   # False
```

---

## non_empty

Return True if value contains at least one non-whitespace character.

### Parameters

- `value` (`str`): The string to check for non-whitespace content.

### Returns

- `bool`: True if `value` contains at least one non-whitespace character, otherwise False.

### Example

```python
from validators import non_empty

print(non_empty("hello"))     # True
print(non_empty("   "))       # False
print(non_empty(""))          # False
print(non_empty(" a "))       # True
```
