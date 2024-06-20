const express = require('express');

function createRouter(db) {
  const router = express.Router();
  router.get('/book/:type/:startYear/:endYear/:limit/:genre', function (req, res, next) {
    let query = '';
    let startYear = req.params.startYear;
    let endYear = req.params.endYear;
    let limit = req.params.limit.toString();
    let genre = req.params.genre == "Any Genre" ? '%' : req.params.genre;
    switch(req.params.type) {
      case "Most Popular":
        query = `select book.id, title, publisher, aggregate_rating, total_scores, cover, genreID, genre, first_name, middle_names, last_name from book join book_genre on book.id = book_genre.bookID join genre ON genre.id = genreID join book_author on book.id=book_author.bookID join author on author.id = book_author.authorID WHERE pub_date < "${endYear}-01-01" AND pub_date >= "${startYear}-01-01" AND genre LIKE "${genre}" order by total_scores desc, book.id asc, title asc limit ${limit};`
        break;
      case "Worst-Rated":
        query = `select book.id, title, publisher, aggregate_rating, total_scores, cover, genreID, genre, first_name, middle_names, last_name from book join book_genre on book.id = book_genre.bookID join genre ON genre.id = genreID join book_author on book.id=book_author.bookID join author on author.id = book_author.authorID WHERE pub_date < "${endYear}-01-01" AND pub_date >= "${startYear}-01-01" AND genre LIKE "${genre}" order by aggregate_rating asc, book.id asc, title asc limit ${limit}`;
        break;
      default:
        query = `select book.id, title, publisher, aggregate_rating, total_scores, cover, genreID, genre, first_name, middle_names, last_name from book join book_genre on book.id = book_genre.bookID join genre ON genre.id = genreID join book_author on book.id=book_author.bookID join author on author.id = book_author.authorID WHERE pub_date < "${endYear}-01-01" AND pub_date >= "${startYear}-01-01" AND genre LIKE "${genre}" order by aggregate_rating desc, book.id asc, title asc limit ${limit}`;
    }
    console.log(req.params);
    db.query(
      query,
      (error, results) => {
        if (error) {
          console.log(error);
          res.status(500).json({status: 'error'});
        } else {
          res.status(200).json(results);
        }
      }
    );
  });

  return router;
}

module.exports = createRouter;