# Small string helpers used across the example utility library.

## slugify

Convert text to a lowercase, hyphen-separated URL slug.

Non-alphanumeric runs collapse to a single hyphen and leading/trailing hyphens are stripped.

### Parameters

- `text` (`str`): The input string to convert to a slug.

### Returns

- `str`: The slugified version of the input text.

### Example

```python
from string_helpers import slugify

print(slugify("Hello, World!"))  # Output: "hello-world"
print(slugify("  Python_is awesome!!  "))  # Output: "python-is-awesome"
```

---

## truncate

Truncate text to at most limit characters, appending suffix if cut.

### Parameters

- `text` (`str`): The input string to truncate.
- `limit` (`int`): Maximum number of characters allowed in the result. Must be non-negative.
- `suffix` (`str`, optional): String to append if truncation occurs. Defaults to `"..."`.

### Returns

- `str`: The truncated string, possibly with suffix appended.

### Example

```python
from string_helpers import truncate

print(truncate("This is a long sentence.", 10))  # Output: "This is..."
print(truncate("Short", 10))  # Output: "Short"
print(truncate("Hello world", 5, "!"))  # Output: "He!"
```

---

## word_count

Return the number of whitespace-separated words in text.

### Parameters

- `text` (`str`): The input string whose words are to be counted.

### Returns

- `int`: The number of whitespace-separated words in the input text.

### Example

```python
from string_helpers import word_count

print(word_count("Hello world"))  # Output: 2
print(word_count("  Multiple   spaces between words "))  # Output: 5
print(word_count(""))  # Output: 0
```