FetchFugu
==========

**FetchFugu** is a set of two scripts which probably can turn [TextFugu](http://textfugu.com/) into an EPub ebook.

Setup
-----

1. Install required python modules

```
python3 -m pip install -r requirements.txt
``` 

2. Install Pandoc from https://github.com/jgm/pandoc/releases/latest


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
* [PyYAML](http://pyyaml.org/)
* [Pandoc](http://pandoc.org/)