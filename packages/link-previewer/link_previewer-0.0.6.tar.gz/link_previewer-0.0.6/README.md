This package creates a link preview of a URL. This largely relies on the Open Graph protocol proposed by Facebook.

# Installation
```bash
$ pip install link-previewer
```

# Usage
```bash
>>> from previewer import get_preview
>>> url = "https://youtube.com"
>>> preview_info = get_preview(url)
>>> get_preview(url)
final url is:  https://youtube.com
{'title': 'YouTube', 'description': 'Enjoy the videos and music that you love, upload original content and share it all with friends, family and the world on YouTube.', 'url': 'www.youtube.com', 'img_url': 'https://www.youtube.com/img/desktop/yt_1200.png'}

```
# Developing link-previewer 
To install link-previewer, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
$ pip install -e .[dev]
```




