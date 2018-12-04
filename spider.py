import urllib.request
import urllib.error
import sqlite3
import re

class Tumblr(object):
	def __init__(self, like_url, start_page):

		proxies = {"http": "http://127.0.0.1:1080", "https": "http://127.0.0.1:1080"}
		proxy_handler = urllib.request.ProxyHandler(proxies)
		opener = urllib.request.build_opener(proxy_handler)
		urllib.request.install_opener(opener)
		self.__likes_url = like_url
		self.__page = start_page
		self.__root_dir = 'C:\\Users\\Zhenyu\\Downloads\\Tumblr\\1024studio\\'

	def launch(self):
		while True:
			content = self.__request_likes(self.__page)
			frams = self.__get_frame_url(content)
			for fram in frams:
				target_image_urls = self.__get_image_url(fram)
				for image_url in target_image_urls:
					self.__download_image(image_url)
			for fram in frams:
				target_video_urls = self.__get_video_url(fram)
				for video_url in target_video_urls:
					self.__download_video(video_url)
			self.__page = self.__page + 1


	def __do_request(self, url_):
		req = urllib.request.Request(url_)
		res = urllib.request.urlopen(req)
		return res.read().decode('utf-8')

	def __request_likes(self, page):
		print('Request page = %s' % page)
		target_url = self.__likes_url.format(page)
		return self.__do_request(target_url)

	def __get_frame_url(self, content):
		reg = r"(?<=iframe src=')\S*(?=')"
		pattern = re.compile(reg)
		results = pattern.findall(content)
		print('Find results = %s' % len(results))
		return results

	def __get_video_url(self, url_):
		reg = r'((?<=<source src=").*(?=" type="video/mp4"))'
		pattern = re.compile(reg)
		content = self.__do_request(url_)
		result = pattern.findall(content)
		print('Find video URL = %s' % result)
		return result
	
	def __get_image_url(self, url_):
		reg = r'((?<=<source src=").*(?=" type="image/jpg"))'
		pattern = re.compile(reg)
		content = self.__do_request(url_)
		result = pattern.findall(content)
		print('Find image URL = %s' % result)
		return result

	def __download_video(self, url_):
		pattern = re.compile(r'([^/]+$)')
		file_name = pattern.findall(url_)[0]
		dir_ = self.__root_dir + file_name + '.mp4'
		try:
			print('Download: %s ' % url_)
			self.urlretrieve = urllib.request.urlretrieve(url_, dir_)
		except Exception as e:
			print(e)

	def __download_image(self, url_):
		pattern = re.compile(r'([^/]+$)')
		file_name = pattern.findall(url_)[0]
		dir_ = self.__root_dir + file_name + '.jpg'
		try:
			print('Download: %s ' % url_)
			self.urlretrieve = urllib.request.urlretrieve(url_, dir_)
		except Exception as e:
			print(e)

#url => https://xxx.tumblr.com/page/{} 
#page => from 0
#
ins = Tumblr('https://Guanse.tumblr.com/page/{}', 0)
ins.launch()
