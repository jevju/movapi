#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import json
import requests
import re

class Movie():
    def __init__(self, movid, nor = False):

        self.movid = movid
        RT = True

        self.movie = {
            'imdbID':       None,
            'title':        None,
            'year':         None,
            'stars':        None,
            'cast':         None,
            # 'characters':   None,
            'directors':    None,
            'production_company': None,
            'writers':      None,
            'genres':       None,
            'duration':     None,
            'plot_short':   None,
            'plot_long':    None,
            'rating':       None,
            'awards':       None,
            'poster_url':   None,
            'content_rating': None,
            'metascore':    None,
            'recommended':  None,
            'tagline':      None,
            'wikidata_id':  None,
            'rotten_tomatoes': {},
            'metacritic_url': None,
            'metacritic_rating': None,
        }

        self.error = []

        pattern = '^[t]{2}[0-9]{7}$'

        if re.search(pattern, self.movid):
            url = "http://www.imdb.com/title/" + self.movid
            # url = "https://13.32.221.251:443/title/" + self.movid

            self.soup = self.__create_soup(url)

            self.imdbID()
            self.title()
            self.year()
            self.stars()
            self.cast()
            self.directors()
            self.production_company()
            self.writers()
            self.genres()
            self.duration()
            self.plot_long()
            self.plot_short()
            self.rating()
            self.awards()
            self.poster()
            self.content_rating()
            self.metascore()
            # self.trailer()
            self.recommended()
            self.tagline()

            # if nor:
            #     self.soup_nor = self.__create_soup(url, nor=True)
            #     self.movie['title_nor'] = None
            #     self.title_nor()

            # if RT:

                # print(self.wiki_soup)
            self.wikidata()
                # self.rotten_tomatoes_url()
            self.rotten_tomatoes_rating()
            self.metacritic()



            self.print_error_msg()

        else:
            print("Movapi: Movie id ''" + self.movid + "' not valid")

    def formatted_json(self):
        return json.dumps(self.movie, indent = 4, ensure_ascii=False)

    def print_error_msg(self):
        if len(self.error):
            print(str(len(self.error)) + " fields not found for '" + self.movid + "'")
            for msg in self.error:
                print(msg)
            print()

    def __create_soup(self, url, nor = False):
        request = requests.get(url, headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Accept-Language": "en-US, en;q=0.5"
        })

        if nor:
            request  = requests.get(url, headers  = {"Accept-Language": "no-NO, no;q=0.5"})
        # request  = requests.get(url)

        data = request.text
        soup = BeautifulSoup(data, "html.parser")
        return soup

    def imdbID(self):
        try:
            item = str(self.soup.find(property = 'pageId'))
            sep = '" property'
            rest = item.split(sep)[0]
            sep = 'content="'
            rest = rest.split(sep)[1]
            self.movie['imdbID'] = rest
        except:
            self.error.append("imdbID")

    def title(self):
        try:
            item = self.soup.findAll("div", {"class":"title_wrapper"})[0].h1.getText()
            title = re.split(r'\(([\d]){4}\)', item)[0].strip()
            self.movie['title'] = title
        except:
            self.error.append("title")

    def title_nor(self):
        try:
            item = self.soup_nor.find(itemprop = "name")
            title = str(item.next).strip()
            self.movie['title_nor'] = title
        except:
            self.error.append("title")

    def year(self):
        try:
            item = self.soup.findAll("div", {"class":"title_wrapper"})[0].h1.getText()
            year = re.search(r'\(([\d]){4}\)', item).group().replace('(','').replace(')','')
            self.movie['year'] = year
        except:
            self.error.append("year")

    def stars(self):
        try:
            stars = []
            li = self.soup.find_all('div', {'class':'credit_summary_item'})
            for i in li:
                if 'Stars:' in i.text:
                    for a in i:
                        s = str(a)
                        if 'href="/name' in s:
                            dir = {}
                            dir['name'] = s.split('>')[1].split('<')[0]
                            dir['id'] = s.split('/name/')[1].split('/')[0]
                            stars.append(dir)

            self.movie['stars'] = stars

        except:
            self.error.append("stars")

    def cast(self):
        try:
            cast = []
            li = self.soup.findAll('table', {'class', 'cast_list'})[0].findAll('tr')

            for r in li:
                td = r.findAll('td')
                # print(str(td))
                if 'castlist_label' in str(td):
                    continue
                # if
                c = {}
                for t in td:
                    s = str(t)
                    if 'class' not in s:
                        # print(s)
                        c['id'] = s.split('href="/name/')[1].split('/')[0]
                        c['name'] = s.split('> ')[1].split('\n')[0]
                    if 'class="character"' in s:
                        c['character'] = str(t.text).replace('\n', '').replace('  ', '  ')
                cast.append(c)

            self.movie['cast'] = cast

        except:
            self.error.append("actors")

        # for l in li:
        #     a = l.findAll('a')
        #     for i in a:
        #         s = str(i)
        #         if 'class' not in s:
        #             print(s.split(''))
        # try:
        #     li = self.soup.find_all(itemprop="actor")
        #     templist = []
        #     for idx, item in enumerate(li):
        #         temp = li[idx].get_text()
        #         temp = temp.replace("\n", "")
        #         templist.append(temp.lstrip(' ').rstrip())
        #     self.movie['actors'] = templist
        # except:
        #     self.error.append("actors")

    def characters(self):
        try:
            item = self.soup.findAll(itemprop = "actor")
            ch = self.soup.findAll('td', {'class':'character'})
            templist = []
            for i in range(len(item)):
                tempdict = {}
                tempdict['actor'] = item[i].get_text().replace("\n", "").lstrip(' ').rstrip()
                tempdict['character'] = ch[i].get_text().replace("\n", "").replace("  ", "").lstrip(' ').rstrip()
                templist.append(tempdict)
            self.movie['characters']  = templist
        except Exception as e:
            print(e)
            self.error.append("characters")

    def directors(self):
        try:
            directors = []
            li = self.soup.find_all('div', {'class':'credit_summary_item'})
            for i in li:
                if 'Director' in i.text:
                    for a in i:
                        s = str(a)
                        if 'href="/name' in s:
                            d = {}
                            d['id'] = s.split('/name/')[1].split('/')[0]
                            d['name'] = s.split('>')[1].split('<')[0]
                            directors.append(d)

            self.movie['directors'] = directors

        except:
            self.error.append("directors")

    def production_company(self):
        try:
            companies = []
            temp = self.soup.findAll('div', {'class', 'txt-block'})
            for t in temp:
                h = str(t.find('h4'))
                if 'Production C' in h:
                    a = t.findAll('a')
                    for i in a:
                        s = i.text.strip()
                        if 'See more' in s:
                            continue
                        companies.append(s)
            self.movie['production_company'] = companies

        except:
            self.error.append("production company")

    def writers(self):
        try:
            directors = []
            li = self.soup.find_all('div', {'class':'credit_summary_item'})
            for i in li:
                if 'Writer' in i.text:
                    for a in i:
                        s = str(a)
                        if 'href="/name' in s:
                            d = {}
                            d['id'] = s.split('/name/')[1].split('/')[0]
                            d['name'] = s.split('>')[1].split('<')[0]
                            directors.append(d)

            self.movie['writers'] = directors

        except:
            self.error.append("directors")


    def genres(self):
        try:
            genres = []
            temp = self.soup.findAll('div', {'class', 'inline'})
            for t in temp:
                c = t.find('h4')
                if 'Genres' in str(c):
                    gs = t.findAll('a')
                    for g in gs:
                        genres.append(g.text.strip())
                    break
            self.movie['genres'] = genres
        except:
            self.error.append("genres")

    ## -- Finds duration of movie,
    def duration(self):
        try:
            dur = {}
            temp = self.soup.findAll('time')
            for d in temp:
                t = d.text.strip()
                if 'h' in t:
                    dur['hour'] = t
                else:
                    dur['min'] = t
                dur['stamp'] = str(d).split('datetime="')[1].split('"')[0]
            self.movie['duration'] = dur
        except:
            self.error.append("duration")

    def plot_long(self):
        try:
            self.movie['plot_long'] = self.soup.find('div', {'id': 'titleStoryLine'}).find('p').text.strip().split('\n')[0]
        except:
            self.error.append("plot long")

    def plot_short(self):
        try:
            self.movie['plot_short'] =  self.soup.find('div', {'class': 'summary_text'}).text.strip()
        except:
            self.error.append("plot short")


    def rating(self):
        try:
            li = self.soup.find_all(itemprop="ratingCount")
            ratingCount = li[0].get_text()

            li = self.soup.find_all(itemprop="ratingValue")
            ratingValue = li[0].get_text()

            li = self.soup.find_all(itemprop="bestRating")
            ratingBest = li[0].get_text()

            templist = []
            tempdict1 = {}
            tempdict2 = {}
            tempdict3 = {}

            tempdict1['value'] = ratingValue
            tempdict2['count'] = ratingCount
            tempdict3['best'] = ratingBest

            templist.append(tempdict1)
            templist.append(tempdict2)
            templist.append(tempdict3)

            self.movie['rating'] = templist
        except:
            self.error.append("rating")

    def awards(self):
        try:
            li = self.soup.find_all("span", itemprop="awards")
            templist = []
            for i in li:
                u = (i.get_text().replace('.',''))
                u = re.sub("\s\s+", " ", u)
                templist.append(u.lstrip(' ').rstrip())
            self.movie['awards'] = templist
        except:
            self.error.append("awards")

    def poster(self):
        try:
            li = self.soup.find_all('div', {'class':'poster'})
            for l in li:
                s = str(l)
                if 'src="' in s:
                    self.movie['poster_url'] = s.split('src="')[1].split('"')[0]
        except:
            self.error.append("poster URL")

    def content_rating(self):
        try:
            li = self.soup.find_all(itemprop="contentRating")
            self.movie['content_rating'] = (li[0]['content'])
        except:
            self.error.append("content Rating")


    def metascore(self):
        try:
            temp = self.soup.find("div", { "class" : "metacriticScore score_favorable titleReviewBarSubItem" })
            self.movie['metascore'] = temp.get_text().lstrip().rstrip()
        except:
            self.error.append("metascore")

    # def trailer(self):
    #     try:
    #         temp = self.soup.find(itemprop="trailer")
    #         url = "https://www.imdb.com" + temp['href']
    #         self.movie['trailer'] = url
    #     except:
    #         self.error.append("trailer")
        # print(url)
        # print(temp[0].get('src'))

    def recommended(self):
        try:
            temp = self.soup.findAll("div", {'class', 'rec_item'})
            ids = []
            for i in temp:
                ids.append(i.attrs['data-tconst'])
            self.movie['recommended'] = ids
        except:
            self.error.append('recommended')

    def tagline(self):
        try:
            temp = self.soup.findAll("div", {'class', 'txt-block'})
            for t in temp:
                s = str(t)
                if 'Taglines' in s:
                    self.movie['tagline'] = t.text.split('\n')[2].split('\n')[0].strip()
                    break

        except:
            self.error.append('tagline')

    def wikidata(self):
        try:
            url = "https://www.wikidata.org/w/index.php?search=" + self.movid
            soup = self.__create_soup(url)

            temp = soup.findAll('ul', {'class', 'mw-search-results'})
            for li in temp:
                t = li.findAll('div', {'class', 'mw-search-result-heading'})
                mov = t[0].find('a')
                href = mov.get('href')
                wikidata_id = href.split('/')[2]
                title = str(mov.get('title'))
                tit,year = title.split('|')
                year = year.strip().split(' ')[0].replace('\u200e', '')
                # tit = tit.replace('\u200e', '')

                if (self.movie['year'] == year):
                    self.movie['wikidata_id'] = wikidata_id

                    url = 'https://www.wikidata.org/wiki/' + self.movie['wikidata_id']

                    soup = self.__create_soup(url)

                    try:
                        temp = soup.find('div', {'id': 'P1258'})
                        rotten_tomatoes_url = temp.find('a', {'class':'wb-external-id external'}).get('href')
                        self.movie['rotten_tomatoes']['url'] = rotten_tomatoes_url
                    except:
                        self.error.append('rotten_tomatoes')

                    try:
                        temp = soup.find('div', {'id': 'P1712'})
                        metacritic_url = temp.find('a', {'class':'wb-external-id external'}).get('href')
                        self.movie['metacritic_url'] = metacritic_url
                    except:
                        self.error.append('metacritic')

                else:
                    self.error.append('wikidata')
        except:
            self.error.append('wikidata')

    # def rotten_tomatoes_url(self):
    #     try:
    #         url = 'https://www.wikidata.org/wiki/' + self.movie['wikidata_id']
    #
    #         soup = self.__create_soup(url)
    #
    #         temp = soup.find('div', {'id': 'P1258'})
    #         href = temp.find('a', {'class':'wb-external-id external'}).get('href')
    #
    #         self.movie['rotten_tomatoes']['url'] = href
    #     except:
    #         self.error.append('rotten_tomatoes_url')

    def rotten_tomatoes_rating(self):
        try:
            url = self.movie['rotten_tomatoes']['url']

            soup = self.__create_soup(url)

            rating = {}
            tomatometer = {}
            audience = {}

            try:
                critics = soup.find('div', {'class', 'mop-ratings-wrap__half'})
                tomatometer['score'] = critics.find('span', {'class', 'mop-ratings-wrap__percentage'}).text.strip()
                tomatometer['count'] = critics.find('small', {'class', 'mop-ratings-wrap__text--small'}).text.strip()
            except:
                tomatometer['score'] = None
                tomatometer['count'] = None

            try:
                users = soup.find('div', {'class', 'mop-ratings-wrap__half audience-score'})
                audience['score'] = users.find('span', {'class', 'mop-ratings-wrap__percentage'}).text.strip()
                audience['count'] = users.find('strong', {'class', 'mop-ratings-wrap__text--small'}).text.split('Ratings: ')[1]
            except:
                audience['score'] = None
                audience['count'] = None

            rating['audience'] = audience
            rating['tomatometer'] = tomatometer
            self.movie['rotten_tomatoes']['rating'] = rating

        except:
            self.error.append('rotten_tomatoes_rating')

    def metacritic(self):
        try:
            url = self.movie['metacritic_url']
            # print(url)
            soup = self.__create_soup(url)

            r = soup.find('div', {'id':'videoContainer_wrapper'})
            trailer_url = r.get('data-mcvideourl')

            self.movie['trailer_url'] = trailer_url
        except:
            self.error.append('trailer_url')

        try:
            metacritic_rating = {}
            # score = soup.findAll('div', {'class', 'metascore_w larger '})
            score = soup.select_one('div.metascore_w.larger.movie')
            # print(score.getText())
            metacritic_rating['metascore'] = score.getText()


            user_score = soup.select_one('div.metascore_w.user.larger.movie')
            # print(user_score.getText())
            metacritic_rating['user_score'] = user_score.getText()

            self.movie['metacritic_rating'] = metacritic_rating

        except:
            self.error.append('metacritic_rating')

if __name__ == "__main__":
    movie_id = "tt0499549"
    # print(Movie(movie_id).formatted_json())
    res = Movie(movie_id).formatted_json().replace("'", "´")
    print((res))
    # m = Movie(movie_id, nor = True)
