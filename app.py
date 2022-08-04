# all the imports
     
from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
     
from flask_apscheduler import APScheduler
import requests
from bs4 import BeautifulSoup as bs
import PyRSS2Gen
import datetime

header = {
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'
}

rss = PyRSS2Gen.RSS2(
        title = "HMC NEWS",
        link = "Naver.com",
        description = "HMC NEWS",
        lastBuildDate = datetime.datetime.now(),
        items = [] )

rss2 = PyRSS2Gen.RSS2(
        title = "KMC NEWS",
        link = "Naver.com",
        description = "KMC NEWS",
        lastBuildDate = datetime.datetime.now(),
        items = [] )

urls_hmc = ["https://m.search.naver.com/search.naver?where=m_news&query=%ED%98%84%EB%8C%80%EC%9E%90%EB%8F%99%EC%B0%A8&sm=mtb_opt&sort=0&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=&office_section_code=&news_office_checked=&nso=",
'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=%ED%98%84%EB%8C%80%EC%9E%90%EB%8F%99%EC%B0%A8&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=30&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all&start=16',
'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=%ED%98%84%EB%8C%80%EC%9E%90%EB%8F%99%EC%B0%A8&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=61&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all&start=31',
'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=%ED%98%84%EB%8C%80%EC%9E%90%EB%8F%99%EC%B0%A8&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=84&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all&start=46']

urls_kmc = ['https://m.search.naver.com/search.naver?sm=mtb_hty.top&where=m_news&oquery=%EA%B8%B0%EC%95%84%EC%9E%90%EB%8F%99%EC%B0%A8&tqi=h4Wf5lp0JWwssvpxpLVssssstIZ-363433&query=%EA%B8%B0%EC%95%84%EC%9E%90%EB%8F%99%EC%B0%A8&nso=so%3Ar%2Cp%3Aall&mynews=0&office_section_code=0&office_type=0&pd=0&photo=0&sort=0',
'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=%EA%B8%B0%EC%95%84%EC%9E%90%EB%8F%99%EC%B0%A8&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=20&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all&start=16',
'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=%EA%B8%B0%EC%95%84%EC%9E%90%EB%8F%99%EC%B0%A8&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=39&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all&start=31',
'https://m.search.naver.com/search.naver?where=m_news&sm=mtb_pge&query=%EA%B8%B0%EC%95%84%EC%9E%90%EB%8F%99%EC%B0%A8&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=62&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:r,p:all&start=46',
]

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read().decode('utf-8'))
        db.commit()

# configuration
DATABASE = './tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

conn = sqlite3.connect(DATABASE)

with sqlite3.connect(DATABASE) as conn:
    c = conn.cursor()
    c.execute('delete from entries')
    conn.commit()

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/hmc')
def hmc():
    # cur = g.db.execute('select title, text from entries order by id desc')
    # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    # return render_template('show_entries.html', entries=entries)
    return render_template('hmcnews.xml')

@app.route('/kmc')
def kmc():
    # cur = g.db.execute('select title, text from entries order by id desc')
    # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    # return render_template('show_entries.html', entries=entries)
    return render_template('kmcnews.xml')

def check_d(link):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        cur = c.execute(f'select * from entries where link = "{link}"')
        return cur.fetchall()

def check_d2(link):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        cur = c.execute(f'select * from entries2 where link = "{link}"')
        return cur.fetchall()

def get_hmc():
    with requests.Session() as s:
        for url_hmc in urls_hmc:
            html_hmc = s.get(url_hmc, headers=header)
            soup = bs(html_hmc.text,'html.parser')

            for i in soup.find_all( class_ = 'news_wrap'):            
                link = i.find( class_ = 'news_tit')['href']
                title = i.find( class_ = 'news_tit').text
                press = i.find( class_ = 'info press').text
                print(f'{link} [{press}] {title}')
                html_body = s.get(link, headers=header)
                soup_body = bs(html_body.text,'html.parser')
                content = str(soup_body.find(class_ = 'newsct_article _article_body'))
                # print(content)
                if title == None:
                    continue
                if check_d(link) == []:
                    with sqlite3.connect(DATABASE) as conn:
                        c = conn.cursor()
                        c.execute('insert into entries (title,link,date,text) values(?,?,?,?)',(title,link,datetime.datetime.now(),content))
                        conn.commit()                   
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        cur = c.execute('select title, link, date, text from entries order by date desc limit 300')
        fetch = cur.fetchall()
        cur2 = c.execute("DELETE FROM entries WHERE date <=  datetime('now', '-5 days')")
        conn.commit()
        for title,link,date,text in fetch:
            item = PyRSS2Gen.RSSItem(
                        title = title,
                        link = link,
                        guid = PyRSS2Gen.Guid(link,0),
                        description= text,
                        pubDate = date)
            rss.items.append(item)
    rss.write_xml(open('./templates/hmcnews.xml', 'w', -1, "UTF-8"), encoding = 'UTF-8')


def get_kmc():
    with requests.Session() as s:
        for url_hmc in urls_kmc:
            html_hmc = s.get(url_hmc, headers=header)
            soup = bs(html_hmc.text,'html.parser')

            for i in soup.find_all( class_ = 'news_wrap'):            
                link = i.find( class_ = 'news_tit')['href']
                title = i.find( class_ = 'news_tit').text
                press = i.find( class_ = 'info press').text
                print(f'{link} [{press}] {title}')
                html_body = s.get(link, headers=header)
                soup_body = bs(html_body.text,'html.parser')
                content = str(soup_body.find(class_ = 'newsct_article _article_body'))
                # print(content)
                if title == None:
                    continue   
                if check_d2(link) == []:
                    with sqlite3.connect(DATABASE) as conn:
                        c = conn.cursor()
                        c.execute('insert into entries2 (title,link,date,text) values(?,?,?,?)',(title,link,datetime.datetime.now(),content))
                        conn.commit()
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        cur = c.execute('select title, link, date, text from entries2 order by date desc limit 300')
        fetch = cur.fetchall()
        cur2 = c.execute("DELETE FROM entries2 WHERE date <=  datetime('now', '-5 days')")
        conn.commit()
        for title,link,date,text in fetch:
            item = PyRSS2Gen.RSSItem(
                        title = title,
                        link = link,
                        guid = PyRSS2Gen.Guid(link,0),
                        description= text,
                        pubDate = date)
            rss.items.append(item)
    rss2.write_xml(open('./templates/kmcnews.xml', 'w', -1, "UTF-8"), encoding = 'UTF-8')

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.add_job(func=get_hmc, trigger='interval', id='job3', minutes=2, next_run_time=datetime.datetime.now())
scheduler.add_job(func=get_kmc, trigger='interval', id='job4', minutes=2, next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=1))
scheduler.start()

if __name__ == '__main__':
    # init_db()    
    app.run()
