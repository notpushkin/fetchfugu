FetchFugu
==========

**FetchFugu** is a set of two scripts which probably can turn [TextFugu](http://textfugu.com/) into an EPub ebook.

Usage
------

In auth.yml:
```yaml
username: iamale
password: 1t1sl0ng4ndc00l
# replace with your login/pass
```

```
python3 grab.py
python3 epub.py
```

Dependencies
-------------

* [Python 3](https://www.python.org/)
* [python-requests](http://python-requests.org/)
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/)
* [Bleach](http://bleach.readthedocs.org/)
* [Pandoc](http://pandoc.org/)