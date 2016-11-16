import curl
import re

SEPTEMBER=1609

class FreeFoodScraper(object):
    def __init__(self):
        url = "https://lists.princeton.edu/cgi-bin/wa?A1=ind{month_num}&L=freefood&X=2BE54FB0F41980A98B&Y=chay%40princeton.edu".format(month_num=SEPTEMBER)
        curler = curl.Curl(url)
        body = curler.get()
        emails = re.findall("""<span onmouseover="showDesc\('.*?</span>""", body)
        self.email_list = []
        for email in emails:
            content = re.findall("""onmouseover=\".*?[^\\\\]\"""", email)[0].lstrip('showDesc(').rstrip(')')
            sections = re.findall("\'.*?[^\\\\]\'", content)
            try:
                body, title, time = sections
                cleaned_body = body[1:-1].split('-----&lt;br&gt;You are receiving this email')[0]
                self.email_list.append({'body':cleaned_body,
                                        'title':title[1:-1],
                                        'time':time[1:-1]})

            except ValueError:
                print 'ERROR'
                print 'ERROR'
                print email, '\n'
                print content
                print sections
                print 'ERROR'
                print 'ERROR\n'
    def get_all(self):
        return self.email_list
