from scrapy.exceptions import DropItem
from datetime import datetime
import mysql.connector


class MySqlPipeline:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='******'
        )

        self.cursor = self.connection.cursor()

        # Create table if none exists
        databaseName = "book_marks"

        try:
            self.cursor.execute(
                "DROP DATABASE IF EXISTS {}".format(databaseName))
        except mysql.connector.Error as error_descriptor:
            print("Failed dropping database: {}".format(error_descriptor))
            exit(1)

        try:
            self.cursor.execute("CREATE DATABASE {}".format(databaseName))
        except mysql.connector.Error as error_descriptor:
            print("Failed creating database: {}".format(error_descriptor))
            exit(1)

        try:
            self.cursor.execute("USE {}".format(databaseName))
        except mysql.connector.Error as error_descriptor:
            print("Failed using database: {}".format(error_descriptor))
            exit(1)
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS book(
                id INT NOT NULL AUTO_INCREMENT,
                title VARCHAR(150) NOT NULL,
                publisher VARCHAR(75),
                pub_date DATE,
                aggregate_rating varchar(2),
                total_scores int,
                cover varchar(510),
                f_nf varchar(2),
                PRIMARY KEY (id)
            )
            """)
        except mysql.connector.Error as error_descriptor:
            if (error_descriptor.errno ==
                    mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR):
                print("Table already exists: {}".format(error_descriptor))
            else:
                print("Failed creating schema: {}".format(error_descriptor))
            exit(1)

        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS author(
                id INT NOT NULL AUTO_INCREMENT,
                first_name VARCHAR(25),
                middle_names VARCHAR(50),
                last_name VARCHAR(25),
                auth_title VARCHAR(8),
                suffix VARCHAR(8),
                PRIMARY KEY (id)
            )
            """)
        except mysql.connector.Error as error_descriptor:
            if (error_descriptor.errno ==
                    mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR):
                print("Table already exists: {}".format(error_descriptor))
            else:
                print("Failed creating schema: {}".format(error_descriptor))
            exit(1)

        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_author(
                bookID int NOT NULL,
                authorID int NOT NULL,
                role VARCHAR(15),
                ordinal CHAR(1),
                FOREIGN KEY (bookID) references book(ID),
                FOREIGN KEY (authorID) references author(ID),
                PRIMARY KEY (bookID, authorID)
            )
            """)
        except mysql.connector.Error as error_descriptor:
            if (error_descriptor.errno ==
                    mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR):
                print("Table already exists: {}".format(error_descriptor))
            else:
                print("Failed creating schema: {}".format(error_descriptor))
            exit(1)

        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS genre(
                ID int NOT NULL AUTO_INCREMENT,
                genre VARCHAR(50),
                PRIMARY KEY (ID)
            )
            """)
        except mysql.connector.Error as error_descriptor:
            if (error_descriptor.errno ==
                    mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR):
                print("Table already exists: {}".format(error_descriptor))
            else:
                print("Failed creating schema: {}".format(error_descriptor))
            exit(1)

        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS book_genre(
                bookID int NOT NULL,
                genreID int NOT NULL,
                FOREIGN KEY (bookID) references book(ID),
                FOREIGN KEY (genreID) references genre(ID),
                PRIMARY KEY (bookID, genreID)
            )
            """)
        except mysql.connector.Error as error_descriptor:
            if (error_descriptor.errno ==
                    mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR):
                print("Table already exists: {}".format(error_descriptor))
            else:
                print("Failed creating schema: {}".format(error_descriptor))
            exit(1)

    def process_item(self, book, spider):
        try:
            self.cursor.execute(
                'select * from book where title = "%s"'
                % book['title'])
            result = self.cursor.fetchone()
        except mysql.connector.Error as error_descriptor:
            print("Failed querying database: {}".format(error_descriptor))

        if result:
            spider.logger.warn("Item already in database: %s" %
                               book['title'])
        else:
            bookId = False
            authorId = False
            seenAuthor = False
            genreId = False
            seenGenre = False
            # Insert statement
            try:
                self.cursor.execute(""" INSERT INTO book
                                    (title, publisher, pub_date, aggregate_rating,
                                    total_scores, cover, f_nf)
                                    values (%s, %s, %s, %s, %s, %s, %s)""", (
                    book['title'],
                    book['publisher'],
                    book['pub_date'],
                    book['aggregate_rating'],
                    book['total_scores'],
                    book['cover'],
                    book['f_nf']
                ))
                bookId = self.cursor.lastrowid
            except mysql.connector.Error as error_descriptor:
                print("Failed inserting tuple into book: {}".format(
                    error_descriptor))
            if bookId:
                for author in book['authors']:
                    try:
                        self.cursor.execute(
                            'select * from author WHERE first_name = "{}" AND last_name = "{}"'.format(
                                author[0], author[2]
                            ))
                        result = self.cursor.fetchone()
                    except mysql.connector.Error as error_descriptor:
                        print("Failed querying database: {}".format(
                            error_descriptor))
                    if result:
                        seenAuthor = result[0]
                        spider.logger.warn("Item already in database: {} {}".format(
                            author[0], author[2]))
                    else:
                        try:
                            self.cursor.execute(""" INSERT INTO author
                                                (first_name, middle_names, last_name, auth_title, suffix)
                                                values (%s, %s, %s, %s, %s)""", (
                                author[0],
                                author[1],
                                author[2],
                                author[3],
                                author[4]
                            ))
                        except mysql.connector.Error as error_descriptor:
                            print("Failed inserting tuple into author: {}".format(
                                error_descriptor))
                    if seenAuthor:
                        authorId = seenAuthor
                    else:
                        authorId = self.cursor.lastrowid
                    try:
                        self.cursor.execute(""" INSERT INTO book_author
                                            (bookID, authorID, role, ordinal)
                                            values (%s, %s, %s, %s)""", (
                            bookId,
                            authorId,
                            author[5],
                            author[6],
                        ))
                    except mysql.connector.Error as error_descriptor:
                        print("Failed inserting tuple into book_author: {}".format(
                            error_descriptor))
                for genre in book['genres']:
                    try:
                        self.cursor.execute(
                            'select * from genre WHERE genre = "{}"'.format(
                                genre
                            ))
                        result = self.cursor.fetchone()
                    except mysql.connector.Error as error_descriptor:
                        print("Failed querying database: {}".format(
                            error_descriptor))
                    if result:
                        seenGenre = result[0]
                        spider.logger.warn("Item already in database: {}".format(
                            genre))
                    else:
                        try:
                            self.cursor.execute(""" INSERT INTO genre
                                                (genre)
                                                values ('{}')""".format(genre),)
                        except mysql.connector.Error as error_descriptor:
                            print("Failed inserting tuple into genre: {}".format(
                                error_descriptor))
                    if seenGenre:
                        genreId = seenGenre
                    else:
                        genreId = self.cursor.lastrowid
                    try:
                        self.cursor.execute(""" INSERT INTO book_genre
                                            (bookID, genreID)
                                            values (%s, %s)""", (
                            bookId,
                            genreId
                        ))
                    except mysql.connector.Error as error_descriptor:
                        print("Failed inserting tuple into book_genre: {}".format(
                            error_descriptor))
        self.connection.commit()
        return book

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()


class CheckItemPipeline(object):
    def process_item(self, book, spider):
        if (not book['title'] or not book['publisher']):
            raise DropItem['Missing something!']
        return book


class CleanDatePipeline:
    def process_item(self, book, spider):
        book['title'] = book['title'][0].replace(
            "\u2014", "-").replace("\u2019", "'")
        book['publisher'] = book['publisher'].replace(
            "\u2014", "-").replace("\u2019", "'")
        scoreDict = {
            'Rave': 4,
            'Positive': 3,
            'Mixed': 2,
            'Pan': 1
        }
        book['aggregate_rating'] = scoreDict[book['aggregate_rating']]
        for i, author in enumerate(book['authors']):
            for j, data in enumerate(author):
                if data == '':
                    book['authors'][i][j] = None
        return book
