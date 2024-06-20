import { Component } from '@angular/core';
import { FormGroup } from '@angular/forms';
import {provideNativeDateAdapter} from '@angular/material/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { ServerService } from './server.service';
import { MdbDropdownModule } from 'mdb-angular-ui-kit/dropdown';
import { MdbRippleModule } from 'mdb-angular-ui-kit/ripple';
import {MatDatepickerModule, MatDatepickerInputEvent } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, MdbDropdownModule, MdbRippleModule, MatDatepickerModule, MatFormFieldModule, MatInputModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  providers: [provideNativeDateAdapter()]

})
export class AppComponent {
  books: any[] = [];
  selector: String = 'Best-Rated';
  genre: String = 'Any Genre';
  genreList: String[] = [
    "Any Genre",
    "Fiction",
    "Literary",
    "Essays",
    "Non-Fiction",
    "Politics",
    "Nature",
    "History",
    "Biography",
    "Memoir",
    "Historical",
    "Romance",
    "Literature in Translation",
    "Story Collections",
    "Mystery, Crime, & Thriller",
    "Film & TV",
    "Fantasy",
    "Graphic Novels",
    "Speculative",
    "Technology",
    "Poetry",
    "Investigative Journalism",
    "Graphic Nonfiction",
    "Science",
    "Social Sciences",
    "Criticism",
    "Culture",
    "Art",
    "Music",
    "Religion",
    "Travel",
    "LGBTQ Stories",
    "Sports",
    "Horror",
    "Sci-Fi and Fantasy",
    "True Crime",
    "Health"
  ]
  startYear: String = '1900';
  endYear: String = '2100';

  constructor( private server: ServerService) { }

  ngOnInit() {
    this.getBooks();
  }

  private getBooks() {
    this.books = [];
    this.server.getBooks(this.selector, this.genre, this.startYear, this.endYear).then((response: any) => {
      console.log('Response', response);
      let currentID: number = 0;
      response.forEach((book: { id: number, genres: string[], genre: string, author: string; first_name: any; middle_names: any; last_name: any; }) => {
        if (currentID == book.id) {
          this.books[this.books.length - 1].genres.push(book.genre);
        } else {
          book.genres = [book.genre];
          book.author = `${book.first_name ? book.first_name : ''} ${book.middle_names ? book.middle_names : ''} ${book.last_name ? book.last_name : ''}`;
          this.books.push(book);
        }
        currentID = book.id;
      });
    });
  }

  public toggleChartSelect(e: any) {
    this.selector = e.target.id;
    this.getBooks();
  }

  public toggleGenreSelect(e: any) {
    this.genre = e.target.id;
    this.getBooks();
  }

  public toggleDate(button: String, e: any) {
    if (button == 'start') {
      this.startYear = new Date(e.value).toISOString().split('T')[0];
    } else {
      this.endYear = new Date(e.value).toISOString().split('T')[0];
    }
    this.getBooks();
  }
}
