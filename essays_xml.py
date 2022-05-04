import xml.etree.ElementTree as ET
from lxml import etree
from datetime import datetime

source_rss = 'http://www.aaronsw.com/2002/feeds/pgessays.rss'
local_rss = 'pgessays.rss'

# url.urlretrieve(source_rss, local_rss)

tree = ET.parse(local_rss)
root = tree.getroot()

# latest = root[0].find('item')[1].text
# new = ET.fromstring(url.urlopen(source_rss, timeout=10).readlines())



cnt = 0
for item in root.iter('item'):
    cnt += 1
    print(cnt)
    if item.find('description') is None and item[0].text.endswith('html'):
        html_tree = etree.parse(item[0].text, etree.HTMLParser())
        for x in html_tree.xpath("//font"):
            x.attrib.clear()
        des = etree.tostring(html_tree.xpath("//font")[0])
        item.append(ET.Element('description'))
        item[2].text = des.decode()
    if item.find('pubDate') is None:
        item.append(ET.Element('pubDate'))
        item[3].text = datetime.now().strftime("%a, %d %b %Y %X +0800")
        # Sun, 04 Oct 2020 15:17:00 -0700
tree.write(local_rss)