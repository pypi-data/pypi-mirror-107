import argparse
import xml.etree.ElementTree as ET
from dateutil.parser import parse

tree = ET.parse("/Users/jackie/Downloads/录制-16405-20210317-080233-苏醒.xml")
root = tree.getroot()