#!/usr/bin/env python

from __future__ import print_function
import requests
import csv
from datetime import datetime
import os
import shutil



URL = 'http://cache.newsomatic.net/dynamicv2/content/files/feed.php?format=json&token=FreJPn2ZcFXS3NVu' 

HEADERS = ["Headline",
	"Subheadline",
	"MainArticle",
	"MainArticle1-2",
	"MainArticle5-6",
	"MainArticleSpanish"]

HTML_TEMPLATE_START = """<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>News-o-Matic</title>
<style>
/* -------------------------------------
    GLOBAL
------------------------------------- */
* {
  font-family: "Helvetica Neue", "Helvetica", Helvetica, Arial, sans-serif;
  font-size: 100%;
  line-height: 1.6em;
  margin: 0;
  padding: 0;
}
img {
  max-width: 600px;
  width: auto;
}
body {
  -webkit-font-smoothing: antialiased;
  height: 100%;
  -webkit-text-size-adjust: none;
  width: 100% !important;
}
/* -------------------------------------
    ELEMENTS
------------------------------------- */
a {
  color: #348eda;
}
.btn-primary {
  Margin-bottom: 10px;
  width: auto !important;
}
.btn-primary td {
  background-color: #348eda; 
  border-radius: 25px;
  font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif; 
  font-size: 14px; 
  text-align: center;
  vertical-align: top; 
}
.btn-primary td a {
  background-color: #348eda;
  border: solid 1px #348eda;
  border-radius: 25px;
  border-width: 10px 20px;
  display: inline-block;
  color: #ffffff;
  cursor: pointer;
  font-weight: bold;
  line-height: 2;
  text-decoration: none;
}
.last {
  margin-bottom: 0;
}
.first {
  margin-top: 0;
}
.padding {
  padding: 10px 0;
}
/* -------------------------------------
    BODY
------------------------------------- */
table.body-wrap {
  padding: 20px;
  width: 100%;
}
table.body-wrap .container {
  border: 1px solid #f0f0f0;
}
/* -------------------------------------
    FOOTER
------------------------------------- */
table.footer-wrap {
  clear: both !important;
  width: 100%;  
}
.footer-wrap .container p {
  color: #666666;
  font-size: 12px;
  
}
table.footer-wrap a {
  color: #999999;
}
/* -------------------------------------
    TYPOGRAPHY
------------------------------------- */
h1, 
h2, 
h3 {
  color: #111111;
  font-family: "Helvetica Neue", Helvetica, Arial, "Lucida Grande", sans-serif;
  font-weight: 200;
  line-height: 1.2em;
}
h1 {
  font-size: 36px;
  margin: 0px 0 0px;
}
h2 {
  font-size: 28px;
  margin: 40px 0 10px;
}
h3 {
  font-size: 22px;
  margin: 40px 0 10px;
}
p, 
ul, 
ol {
  font-size: 14px;
  font-weight: normal;
  margin-bottom: 10px;
}
ul li, 
ol li {
  margin-left: 5px;
  list-style-position: inside;
}
/* ---------------------------------------------------
    RESPONSIVENESS
------------------------------------------------------ */
/* Set a max-width, and make it display as block so it will automatically stretch to that width, but will also shrink down on a phone or something */
.container {
  clear: both !important;
  display: block !important;
  Margin: 0 auto !important;
  max-width: 600px !important;
}
/* Set the padding on the td rather than the div for Outlook compatibility */
.body-wrap .container {
  padding: 20px;
}
/* This should also be a block element, so that it will fill 100% of the .container */
.content {
  display: block;
  margin: 0 auto;
  max-width: 600px;
}
/* Let's make sure tables in the content area are 100% wide */
.content table {
  width: 100%;
}
</style>
</head>

<body bgcolor="#f6f6f6">

<!-- body -->
<table class="body-wrap" bgcolor="#f6f6f6">
  <tr>
    <td></td>
    <td class="container" bgcolor="#FFFFFF">

      <!-- content -->
      <div class="content">
      <table>
        <tr>
          <td>"""

HTML_TEMPLATE_END = """</td>
        </tr>
      </table>
      </div>
      <!-- /content -->
      
    </td>
    <td></td>
  </tr>
</table>
<!-- /body -->

<!-- footer -->
<table class="footer-wrap">
  <tr>
    <td></td>
    <td class="container">
      
      <!-- content -->
      <div class="content">
        <table>
          <tr>
            <td align="center">
              <p>Scraped by Matt Mahowald.</p>
            </td>
          </tr>
        </table>
      </div>
      <!-- /content -->
      
    </td>
    <td></td>
  </tr>
</table>
<!-- /footer -->

</body>
</html>"""

class Article:

	def __init__(self, json_content):
		self.headline = json_content["Headline"]
		self.subhead = json_content["Subheadline"]
		self.main = json_content["MainArticle"]
		self.main_low = json_content["MainArticle1-2"]
		self.main_mid = json_content["MainArticle5-6"]
		self.main_span = json_content["MainArticleSpanish"]
		
	def get_all(self):
		return [self.headline, self.subhead, self.main, 
					self.main_low, self.main_mid, self.main_span]


def get_json_data(URL):
	r = requests.get(URL)
	return r.json()

def write_to_csv(articles):
	with open('news-o-matic.csv', 'w') as csvfile:
		article_writer = csv.writer(csvfile, csv.QUOTE_ALL)
		article_writer.writerow(HEADERS)
		for article in articles:
			article_writer.writerow(article.get_all())
	
def format_spanish(spanish_html):
	spanish_html = spanish_html.replace('<b>', '<h1>', 1)
	spanish_html = spanish_html.replace('\n<i>', '</h1>\n<h2>', 1)
	spanish_html = spanish_html.replace('</i></b>', '</h2>\n<p>', 1)
	return spanish_html
	

def write_to_html(articles):
	for a, n in zip(articles, range(1,len(articles) + 1)):
		data = a.get_all()
		h = data[0]
		h2 = data[1]
		types = ['advanced', 'intermediate', 'starter']
		for i, t in zip(range(2,2+len(types)), types):
			with open('news-o-matic-{}-{}.html'.format(n, t), 'w') as htmlfile:
				#htmlfile.write(HTML_TEMPLATE_START)
				htmlfile.write("<h1>{}</h1>".format(h))
				htmlfile.write("<h2>{}</h2>".format(h2))
				htmlfile.write("<p>{}</p>".format(data[i]))
				#htmlfile.write(HTML_TEMPLATE_END)
		with open('news-o-matic-{}-spanish.html'.format(n), 'w') as htmlfile:
				#htmlfile.write(HTML_TEMPLATE_START)
				htmlfile.write("{}</p>".format(format_spanish(data[5])))
				#htmlfile.write(HTML_TEMPLATE_END)
	
	with open('news-o-matic-aggregated.html', 'w') as htmlfile:
		htmlfile.write(HTML_TEMPLATE_START)
		htmlfile.write("<h1>News-o-Matic feed: {}</h1>".format("{:%B %d, %Y}".format(datetime.now())))
		for a in articles:
			data = a.get_all()
			htmlfile.write("<h2>{}</h2>".format(data[0]))
			htmlfile.write("<h3>{}</h3>".format(data[1]))
			htmlfile.write("<p>{}</p>".format(data[2]))
			htmlfile.write("<p>{}</p>".format(data[3]))
			htmlfile.write("<p>{}</p>".format(data[4]))
			htmlfile.write("<p>{}</p>".format(data[5]))
			
		htmlfile.write(HTML_TEMPLATE_END)


def main():
	print("""Welcome to the News-o-Matic Feed Parser™

Your .html files will be created in a subfolder labeled {:%B %d, %Y}

If the script has stopped working, please type news --help to  
diagnose the issue.
	""".format(datetime.now()))
	folder = "{}/{:%Y-%m-%d}".format(os.getcwd(), datetime.now())
	shutil.rmtree(folder)
	os.mkdir(folder)
	os.chdir(folder)
	data = get_json_data(URL)
	articles = [Article(content) for content in data]
	write_to_csv(articles)
	write_to_html(articles)

if __name__ == '__main__':
	main()
