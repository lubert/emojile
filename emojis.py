import os, requests, grequests
from bs4 import BeautifulSoup

def process_image(r, path):
    with open(path, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)
    r.close()

def get_emojis(team, token):
    url = 'https://{0}.slack.com/api/emoji.list?token={1}'.format(team, token)
    r = requests.get(url)
    if r.status_code == 200:
        emoji = r.json().get('emoji', {})
        target_dir = os.getcwd() + '/%s' % team
        if emoji and not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        image_urls = []
        image_paths = []
        for image_name, image_url in emoji.items():
            if not image_url or image_url.startswith('alias:'):
                continue
            image_ext = image_url.split('.')[-1]
            image_path = os.path.join(target_dir,
                                      image_name + '.' + image_ext)
            if not os.path.exists(image_path):
                image_urls.append(image_url)
                image_paths.append(image_path)

        rs = (grequests.get(u) for u in image_urls)
        responses = grequests.map(rs)

        for response, path in zip(responses, image_paths):
            process_image(response, path)

def post_emojis(team, cookie):
    url = "https://{}.slack.com/customize/emoji".format(team)
    target_dir = os.getcwd() + '/%s' % team
    for filename in os.listdir(target_dir):
        print("Processing {}.".format(filename))
        
        emoji_name = os.path.splitext(os.path.basename(filename))[0]
        
        s = requests.Session()
        s.headers.update({
            'Pragma': 'no-cache',
            'Origin': 'null',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8,de;q=0.6',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.49 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Cookie': cookie
        })

        # Fetch the form first, to generate a crumb.
        res = s.get(url)
        soup = BeautifulSoup(res.text)
        crumb = soup.find("input", attrs={"name": "crumb"})["value"]
        
        data = {
            'add': 1,
            'crumb': crumb,
            'name': emoji_name,
            'mode': 'data',
        }
        files = {'img': open(target_dir + '/' + filename, 'rb')}
        res = s.post(url, data=data, files=files, allow_redirects=False)
        print("{} complete.".format(filename))
    
