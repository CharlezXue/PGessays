import requests
from lxml import etree
from datetime import datetime


proxies = {
 "http": "http://127.0.0.1:19002",
}

source_rss = 'http://www.aaronsw.com/2002/feeds/pgessays.rss'
local_rss = 'pgessays.rss'

try:
    r = requests.get(source_rss, proxies=proxies)
except:
    exit('Timeout')


remote_root = etree.fromstring(r.content)
remote_items = remote_root[0].findall('item')

local_tree = etree.parse(local_rss, etree.XMLParser(remove_blank_text=True))
local_root = local_tree.getroot()
local_items = local_root[0].findall('item')

diff = len(remote_items) - len(local_items)
print(f'{diff} updated from {len(local_items)} to {len(remote_items)}')

if diff == 0:
    exit()

for i in range(diff):
    new_item = remote_items[diff - i - 1]
    print(f'Add new essay: {new_item[1].text}')
    html_tree = etree.parse(new_item[0].text, etree.HTMLParser())
    for x in html_tree.xpath("//font"):
        x.attrib.clear()
    des = etree.tostring(html_tree.xpath("//font")[0])
    new_item.append(etree.Element('description'))
    new_item.find('description').text = des.decode()
    new_item.append(etree.Element('pubDate'))
    new_item.find('pubDate').text = datetime.now().strftime("%a, %d %b %Y %X +0800")
    local_root[0].insert(3, new_item)  # title, link, des, item

local_tree.write(local_rss, pretty_print=True)


def full_build():
    tree = etree.parse(local_rss)
    root = tree.getroot()
    cnt = 0
    for item in root.iter('item'):
        cnt += 1
        print(cnt)
        if item.find('description') is None and item[0].text.endswith('html'):
            html_tree = etree.parse(item[0].text, etree.HTMLParser())
            for x in html_tree.xpath("//font"):
                x.attrib.clear()
            des = etree.tostring(html_tree.xpath("//font")[0])
            item.append(etree.Element('description'))
            item.find('description').text = des.decode()
        if item.find('pubDate') is None:
            item.append(etree.Element('pubDate'))
            item[3].text = datetime.now().strftime("%a, %d %b %Y %X +0800")
            # Sun, 04 Oct 2020 15:17:00 -0700
    tree.write(local_rss)