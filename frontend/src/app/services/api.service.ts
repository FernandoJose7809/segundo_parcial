import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export const API_BASE_URL = 'http://localhost:8000/api/';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private baseUrl = API_BASE_URL;

  constructor(private http: HttpClient) {}

  private getHeaders() {
    return { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };
  }

  get(endpoint: string): Observable<any> {
    return this.http.get(this.baseUrl + endpoint, this.getHeaders());
  }

  post(endpoint: string, data: any): Observable<any> {
    return this.http.post(this.baseUrl + endpoint, data, this.getHeaders());
  }

  put(endpoint: string, data: any): Observable<any> {
    return this.http.put(this.baseUrl + endpoint, data, this.getHeaders());
  }

  delete(endpoint: string): Observable<any> {
    return this.http.delete(this.baseUrl + endpoint, this.getHeaders());
  }
}
