# AoPy

This is an unofficial package that allows for interacting with the Art of Problem Solving website.
This package is not made by, endorsed, or otherwise affiliated with AoPS Incorporated.
Please remember to abide by the <a href="https://artofproblemsolving.com/company/tos">AoPS Terms of Service</a>.
Please be benevolent and responsible when using this package.

## Example

Note: Syntax is not final.

```python
from aopy import Session
session = Session(True)
print(session.get_forum_threads(170)['response']['category']['category_name'])
```