import urllib.request as url
import xml.etree.ElementTree as ET
from lxml import etree

source_rss = 'http://www.aaronsw.com/2002/feeds/pgessays.rss'
local_rss = 'pgessays.rss'

tree = ET.parse(local_rss)
root = tree.getroot()

# latest = root[0].find('item')[1].text
# new = ET.fromstring(url.urlopen(source_rss, timeout=10).readlines())

for item in root.iter('item'):
    if item.find('description') is None:
        html_tree = etree.parse(item[0].text, etree.HTMLParser())
        des = etree.tostring(html_tree.xpath("//font[@size=2]")[0])
        item.append(ET.Element('description'))
        item[2].text = des.decode()
tree.write(local_rss)