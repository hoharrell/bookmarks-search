import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ServerService {

    constructor(private http: HttpClient) {
    }

    private async request(method: string, url: string, data?: any) {
      console.log(data);
      const result = this.http.get(`${url}/${data.type}/${data.startYear}/${data.endYear}/${data.limit}/${data.genre}`);
      return new Promise((resolve, reject) => {
        result.subscribe(resolve, reject);
      });
    }

    getBooks(selector: String, genre: String, startYear: String, endYear: String) {
      return this.request('GET', `${environment.serverUrl}/book`, {type: selector, startYear, endYear, limit: 50, genre});
    }
}