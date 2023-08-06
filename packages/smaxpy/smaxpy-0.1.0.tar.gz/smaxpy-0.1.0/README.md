# smax

Just a small wrapper to website scraping utilities.

It just wraps around `requests`, `bs4` and `cloudscraper`.

## Install

```
pip3 install smaxpy
```

## Usage

```python
from smaxpy import Smax

a = Smax("https://www.google.com")

print(a.title)
```

**All functions from bs4 are inherited now by `Smax`, so you can use functions such as `find()`, `find_all()` directly.**

#### Using the BeautifulSoup's functions

```python
from smaxpy import Smax

a = Smax("https://www.google.com")

print(a.find("title").text) # similar to `a.title`
```

##

### &copy; 2021 TheBoringDude
