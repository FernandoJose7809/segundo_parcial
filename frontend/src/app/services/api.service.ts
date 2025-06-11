import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export const Apiurl = 'http://127.0.0.1:8000/api/';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(private http: HttpClient) {}

  get(endpoint: string): Observable<any> {
    return this.http.get(Apiurl + endpoint);
  }

  post(endpoint: string, data: any): Observable<any> {
    return this.http.post(Apiurl + endpoint, data);
  }

  put(endpoint: string, data: any): Observable<any> {
    return this.http.put(Apiurl + endpoint, data);
  }

  delete(endpoint: string): Observable<any> {
    return this.http.delete(Apiurl + endpoint);
  }
}
