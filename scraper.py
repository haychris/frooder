import curl
import re
from HTMLParser import HTMLParser


class FreeFoodScraper(object):
    def __init__(self, month_id):
        self.html_parser = HTMLParser()
        key = "4FC1A120A0BE8A7C90"
        netid = "chay"
        url = "https://lists.princeton.edu/cgi-bin/wa?A1=ind{month_id}&L=freefood&X={key}&Y={netid}%40princeton.edu".format(
            month_id=month_id, key=key, netid=netid)
        curler = curl.Curl(url)
        body = curler.get()
        emails = re.findall("""<span onmouseover="showDesc\('.*?</span>""",
                            body)
        self.email_list = []
        for email in emails:
            content = re.findall("""onmouseover=\".*?[^\\\\]\"""",
                                 email)[0].lstrip('showDesc(').rstrip(')')
            sections = re.findall("\'.*?[^\\\\]\'", content)
            try:
                body, title, time = sections
                cleaned_body = body[1:-1].split(
                    '-----&lt;br&gt;You are receiving this email')[0]
                self.email_list.append({
                    'body': self.html_cleaner(cleaned_body),
                    'title': self.html_cleaner(title[1:-1]),
                    'time': self.html_cleaner(time[1:-1])
                })

            except ValueError:
                print 'ERROR'
                print 'ERROR'
                print email, '\n'
                print content
                print sections
                print 'ERROR'
                print 'ERROR\n'

    def html_cleaner(self, txt):
        escaped = self.html_parser.unescape(txt.decode('utf8'))
        replaced = escaped.replace('<br>', '\n')
        stripped = replaced.rstrip().lstrip()
        return stripped

    def get_all(self):
        return self.email_list
