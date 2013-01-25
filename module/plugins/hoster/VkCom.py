# -*- coding: utf-8 -*-

import re
from module.plugins.Hoster import Hoster
from module.unescape import unescape

class VkCom(Hoster):
    __name__ = "VkCom"
    __type__ = "hoster"
    __pattern__ = r"http://(www\.)?vk.com/video_ext.php/\?oid="
    #http://vk.com/video_ext.php?oid=166335015&id=162608895&hash=b55affa83774504b&hd=1
    __version__ = "0.1"
    __description__ = """Vk.com Video Download Hoster"""
    __author_name__ = ("vonpupp")
    __author_mail__ = ("vonpupp@gmail.com")
        
    def setup(self):
        self.html = None
        
    def process(self, pyfile):
        self.pyfile = pyfile
        self.download_html()
        pyfile.name = self.get_file_name()
        self.download(self.get_file_url())
        import ipdb; ipdb.set_trace()

    def download_html(self):
        self.html = self.load(self.pyfile.url)
        import ipdb; ipdb.set_trace()

    def get_file_url(self):
        videoId = re.search(r"addVariable\('_videoid','(.*)'\);p.addParam\('quality'", self.html).group(1)
        videoServer = re.search("rel='image_src' href='(.*)thumbs/.*' />", self.html).group(1)
        file_url = videoServer + videoId + ".flv"
        return file_url

    def get_file_name(self):
        file_name_pattern = r"<h1 class='globalHd'>(.*)</h1>"
        return unescape(re.search(file_name_pattern, self.html).group(1).replace("/", "") + '.flv')

    def file_exists(self):
        self.download_html()
        self.load(str(self.pyfile.url), cookies=False, just_header=True)
        if self.req.lastEffectiveURL == "http://www.myvideo.de/":
            return False
        return True
