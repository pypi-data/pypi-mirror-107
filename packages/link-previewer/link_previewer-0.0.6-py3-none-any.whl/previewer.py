import tldextract
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import sys

def valid(title):
    """
    Checks if the title(or any string) is greater than 3 characters.
    """
    if title != None and len(title) > 3:
        return True
    return False

def extract_title(soup):
    """
    Searches through the soup and finds the appropriate description.
    Note: Try using fb:description as well.
    """
    try:
        title = soup.find('meta', property="og:title")['content']
        #twitter_title = soup.find('meta', attrs={'property':'twitter:title'})['content']
        if valid(title):
            return title, True
    except:
        pass
    try:
        title = soup.find('meta', property='twitter:title')['content']
        if valid(title):
            return title, True
    except:
        pass
    try:
        title = soup.find('title').text
        if valid(title):
            return title, True
    except:
        pass
    try:
        title = soup.find('h1').text
        if valid(title):
            return title, True
    except:
        pass
    try:
        title = soup.find('h2').text
        if valid(title):
            return title, True
    except:
        pass
    return None, False

# extract description
def extract_description(soup):
    """
    Searches through the soup and finds the appropriate description.
    Note: Try using fb:description as well.
    """
    try:
        description = soup.find('meta', property="og:description")['content']
        if valid(description):
            return description, True
            pass
    except Exception as e:
        pass
    try:
        description = soup.find('meta', property='twitter:description')['content']
        if valid(description):
            return description, True
            pass
    except Exception as e:
        pass
    try:
        description = soup.find('meta', attrs={'name':'description'})['content']
        if valid(description):
            return description, True
    except Exception as e:
        pass
    try :
        descriptions = soup.find_all('p')
        for description in descriptions:
            if valid(description.text):
                return description.text, True    # return only 200 characters
    except Exception as e:
        pass

    return 'This is the default description of the preview, the link does not follow Open Graph protocol', False

def extract_url(soup, page_url):
    """
    Finds the <link rel="canonical"> or og:url and returns the appropriate url.
    If they don't exist then just return the passed in url as the default url.
    """
    try:
        url = soup.find('meta', property='og:url')['content']
        if valid(url):
            return url, True
    except:
        pass
    try:
        url = soup.find('meta', property='twitter:url')['content']
        if valid(url):
            return url, True
    except:
        pass
    try:
        url = soup.find('link', rel="canonical").text
        if valid(url):
            return url, True
    except:
        pass

    return page_url, False

def finalise_url(soup, url):
    url, found = extract_url(soup, url)
    extract = tldextract.extract(url)
    final_url = 'www.' + extract.domain + '.' + extract.suffix
    return final_url, found

# find the image
def extract_image(soup):
    """
    Get the image from the og:image, or the <link rel="image_src"> or take the image with the largest area
    and width/height ratio in [0.7, 5]
    """
    try:
        image_url = soup.find('meta', property='og:image')['content']
        return image_url, True
    except:
        pass
    try:
        image_url = soup.find('link', rel="img_source")['href']
        return image_url, True
    except:
        pass
    try:
        images = soup.find_all('img')
        prev_img_url = ''
        area = 0
        for img in images:
            try:
                img_url = img['src']
                img = Image.open(urllib.request.urlopen(img_url))
                print(img.width, img.height)
                img_area = img.width * img.height
                ratio = img.width / img.height
                if img_area > area and 0.7 <= ratio <= 5:
                    area = img_area
                    prev_img_url = img_url
                    #print('area is :', area, 'ratio :', ratio)
            except Exception as e:
                pass
        return prev_img_url, True
    except Exception as e:
        pass
    return 'default_img_url', False

def save_html(url, html_file):
    response = requests.get(url)
    if response.status_code == 200:
        with open(html_file, 'wb') as f:
            f.write(response.content)
    else:
        print("There was some error in requesting", url)

def process_url(page_url):
    """
    Finds any anomaly associated with the url. If anomaly found, it tries to correct it else aborts
    """
    info = urlparse(page_url)
    if info.scheme not in ['http', 'https']:
        page_url = 'https://' + page_url
    print("final url is: ", page_url)
    return page_url
def get_preview(page_url):
    page_url = process_url(page_url)
    try:
        html_file_name = 'html_response_file.html'
        save_html(page_url, html_file_name)
        with open(html_file_name, 'rb') as f:
            html_file = f.read()
        soup = BeautifulSoup(html_file, 'lxml')
    except Exception as e:
        sys.stderr.write('Could create an html file, either the url is invalid or you dont have write permissions')
        sys.stdout.write('Using soup directly, without creating an html file...')
        # if this happens work without creating a file. 
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'lxml')      # using lxml parser, later you can make the user choose.

    title, found = extract_title(soup)
    description, found = extract_description(soup)
    url, found = finalise_url(soup, page_url)
    img_url, found = extract_image(soup)

    #sys.stdout.write(title+'\n')
    #sys.stdout.write(description+'\n')
    #sys.stdout.write(url+'\n')
    #sys.stdout.write(img_url+'\n')

    return {"title": title, "description":description, "url":url, "img_url":img_url}

if __name__ == "__main__":
    preview = get_preview('youtube.com')      # youtube is the test url here 
    print(preview)
