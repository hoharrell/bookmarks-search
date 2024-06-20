from scrapy.spiders import SitemapSpider
from bookmarks_crawler.items import Book
from nameparser import HumanName
import re


class BookcrawlerSpider(SitemapSpider):
    name = "bookcrawler"
    allowed_domains = ["bookmarks.reviews"]
    sitemap_urls = [
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-1.xml",
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-2.xml",
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-3.xml",
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-4.xml",
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-5.xml",
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-6.xml",
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-7.xml",
        "https://bookmarks.reviews/wp-sitemap-posts-bookmark-8.xml",]

    # maybe look into this further
    # rules = [Rule(LinkExtractor(allow=r'reviews/(.)*$'),
    #               callback='parse_info', follow=True)]

    def parse(self, response):
        book = Book()
        book['title'] = (response.xpath(
            '//div/h1[@itemprop="name"]/text()').get()),
        book['publisher'] = (response.xpath(
            '//div[@itemprop="publisher"]/span/text()'
        ).get())
        book['pub_date'] = (response.xpath(
            '//div[@itemprop="datePublished"]/@content'
        ).get())
        book['aggregate_rating'] = (response.xpath(
            '//div[@class="book_review_stats"]/div/text()'
        ).get())
        book['total_scores'] = (response.xpath(
            '//span[@itemprop="ratingCount"]/text()'
        ).get())
        book['cover'] = (response.xpath(
            '//div[@class="book_cover"]/img/@src'
        ).get())
        genreList = (response.xpath(
            '//span[@itemprop="genre"]/text()'
        ).getall())
        if (genreList):
            book['f_nf'] = 'f' if genreList[0] == 'Fiction' else 'nf'
        else:
            book['f_nf'] = None
        authors = [(response.xpath(
            '//div[@itemprop="author"]/span[@itemprop="name"]/text()'
        ).get())]
        specialRole = False
        if 'trans.' in authors[0].lower() or 'translated' in authors[0].lower():
            authors = re.split(
                ' and| &|, translated by | translated by |, Translated by|Translated by |Trans\. by |trans\. by |translated by |, trans\. |trans\. ', authors[0])
            print(authors)
            specialRole = 'Translator'
        elif 'ed.' in authors[0].lower() or 'edited' in authors[0].lower():
            authors = re.split(
                ', Ed\. by|, Ed\.|, ed\. by|, ed\.| and| &|, edited by |edited by |, Edited by |Edited by |Ed\. by |ed\. by  |edited by', authors[0])
            specialRole = 'Editor'
        elif 'selected' in authors[0].lower():
            authors = re.split(
                ', selected by |, Selected by| and| &|selected by |Selected by |selected by |Selected by', authors[0])
            specialRole = 'Selector'
        elif ',' in authors[0] or ' and ' or ' & ' in authors[0]:
            authors = re.split(',|and |& ', authors[0])
        authorData = []
        for i, author in enumerate(authors):
            name = HumanName(author)
            if (i > 0 and specialRole) or (len(authors) == 1 and specialRole):
                role = specialRole
            else:
                role = 'Author'
            authorList = [name.first, name.middle,
                          name.last, name.title, name.suffix, role, i]
            authorData.append(authorList)
        book['authors'] = [authorList for authorList in authorData]
        book['genres'] = genreList
        return book
