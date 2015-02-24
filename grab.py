from requests import Session
import yaml
import bs4
from bs4 import BeautifulSoup
import bleach
from urllib.parse import urljoin, urlsplit
import os
import os.path as op
import uuid

config = yaml.load(open("config.yml"))['grabber']
config.update(yaml.load(open(config['auth_file'])))

def AuthSession(username, password):
  s = Session()
  r = s.post("http://www.textfugu.com/wp-login.php", data={
    'log': username,
    'pwd': password,
    'rememberme': "forever",
    'wp-submit': "Log In"
  })
  assert "dashboard" in r.url, "Wrong login or password... probably"
  return s

def parse_lesson_list(s):
  r = s.get("http://www.textfugu.com/lessons/")
  soup = BeautifulSoup(r.text)
  for a in soup.find_all("a", class_=["pn", "pw", "pp"]):
    # print(a)
    yield(urljoin(r.url, a['href']))


class PathMaker:
  def __init__(self):
    self.paths = []
    self._prefixes = []

  def makepath(self, url, index="index"):
    path = tuple(urlsplit(url)[2].strip("/").split("/"))

    if path in self._prefixes:
      path = path + (index,)
    else:
      for i in range(1, len(path)):
        if path[0:i] not in self._prefixes:
          self._prefixes.append(path[0:i])

    return path

  def makepaths(self, urls, **kw):
    # TODO: explain this shit
    for url in sorted(urls, key=len, reverse=True):
      yield (url, self.makepath(url, **kw))


def parse_page(session, url, src_path="", images_prefix="src/images/"):
  r = session.get(url)
  soup = BeautifulSoup(r.text)
  article = soup.find(id="main").article

  # Remove navigation buttons
  for btn in article.find_all(class_="btn"):
    btn.decompose()

  # Fix quotations
  for h4 in article.find_all("h4"):
    try:
      if '“' in h4.string:
        h4.wrap(soup.new_tag("blockquote"))
        h4.unwrap()
    except: pass

  for img in article.find_all("img"):
    image_path = op.join(images_prefix, "%s.%s" % (uuid.uuid4().hex, img['src'].split(".")[-1]))
    real_path = op.join(src_path, image_path)
    os.makedirs(op.dirname(real_path), exist_ok=True)

    picture = session.get(urljoin(r.url, img['src']), stream=True)
    print("         %s" % picture.url)
    print("-------> %s" % real_path)

    with open(real_path, 'wb') as fd:
      for chunk in picture.iter_content(256):
        fd.write(chunk)

    img['src'] = op.abspath(image_path) # if image_path.startswith("/") else "/" + image_path

  # for comment in article.find_all(text=lambda text: isinstance(text, bs4.Comment)):
  #   del comment # TODO!

  tags = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "article", "section",
    "p", "br", "div", "blockquote", "code", "pre", "hr",
    "span", "b", "i", "strong", "em", "tt",
    "ul", "ol", "li", "dd", "dt",
    "img", "a",
    "table", "thead", "tbody", "tfoot", "tr", "th", "td",
    "del", "br", "sup", "sub"
  ]

  attrs = {
    "h1": ["id"],
    "h2": ["id"],
    "h3": ["id"],
    "h4": ["id"],
    "h5": ["id"],
    "h6": ["id"],
    "img": ["src", "alt"],
    "a": ["href", "title"],
    "code": ["class"],
    "p": ["style"]
  }

  return bleach.clean(str(article), tags, attrs, strip=True)


if __name__ == '__main__':
  session = AuthSession(config['username'], config['password'])
  maker = PathMaker()

  with open(config['index_file'], 'w') as index_file:
    lessons = list(parse_lesson_list(session))
    lookup = dict(maker.makepaths(lessons))
    for url in lessons:
      path = lookup[url]
      dest = op.join(config['path'], "/".join(path)) + ".html"

      print("     %s" % url)
      print("---> %s" % dest)

      page = parse_page(session, url)

      os.makedirs(op.dirname(dest), exist_ok=True)
      with open(dest, 'w') as fo:
        fo.write(page)

      index_file.write("%s\n" % dest)
      index_file.flush()