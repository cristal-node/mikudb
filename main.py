#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
import sqlite3
from multiprocessing.pool import ThreadPool



con = sqlite3.connect("mikudb.db")
cur = con.cursor()


pool = []


class mikudb():
	def __init__(self):
		pages_results = ThreadPool(30).imap_unordered(self.page, range(1,self.page_number()+1))
		for r in pages_results:
			print(r)
		print("pool starting!")
		results = ThreadPool(30).imap_unordered(self.article, pool)
		for r in results:
			print(r)

		con.commit()
		cur.close()
		con.close()

	def page_number(self):
		number = BeautifulSoup(requests.get("http://mikudb.moe/type/vocaloid").text, features='lxml').select(".pagination > a:nth-child(12)")[0].attrs["href"].split("/")[-2]
		return int(number)

	def page(self, number):
		url = "http://mikudb.moe/type/vocaloid/page/" + str(number)
		soup = BeautifulSoup(requests.get(url).text, features='lxml').select("#content")[0].select("h4 > a")
		for item in soup:
			link = item.attrs["href"]
			# self.article(link);
			print(f"adding to pool: [{link}]")
			pool.append(link)

	def article(self, url):
		soup = BeautifulSoup(requests.get(url).text, features='lxml')
		title = soup.select(".album-title")[0].string
		# print(title)
		items = BeautifulSoup(str(soup.select(".download-bar > div:nth-child(5) > p:nth-child(1)")[0]).replace("<br/>", "</p><p>"), features='lxml').find_all("p")
		for item in items:
			link = item.a.attrs["href"]
			cloud = item.a.string
			item.a.clear()
			quality = " ".join(str(item.text).replace("\n","").split())
			if len(items) == 1:
				quality = "default"
			print(f"title= [{title}]\nquality= [{quality}]\nlink= [{link}]\ncloud= [{cloud}]")
			self.update(title, quality, cloud, link)
		print(items)
		# dw = soup.select(".download-bar > div:nth-child(5) > p:nth-child(1) > a");
		# print(dw);

	def update(self, title, quality, cloud, link):
		temp_list = [title, quality, cloud, link]
		tp = tuple(temp_list)
		cur.execute('INSERT INTO "main"."albums"("title","quality","cloud","url") VALUES (?,?,?,?);', tp)
		print(f"tuple: [{tp}]")


mikudb();

# url = "http://mikudb.moe/type/vocaloid/page/"

# soup = BeautifulSoup(requests.get(url+"1").text)
# print(soup);

# for i in range(20):
# 	print(i);