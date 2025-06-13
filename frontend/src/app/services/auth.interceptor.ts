import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpInterceptor, HttpHandler, HttpRequest, HttpErrorResponse, HttpClient
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, switchMap } from 'rxjs/operators';
import { API_BASE_URL } from './api.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private http: HttpClient) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const accessToken = localStorage.getItem('access_token');
    let authReq = req;
    if (accessToken) {
      authReq = req.clone({
        setHeaders: { Authorization: `Bearer ${accessToken}` }
      });
    }

    return next.handle(authReq).pipe(
      catchError((error: HttpErrorResponse) => {
        // Evita refrescar el token si la petición es para /token/refresh/
        if (
          error.status === 401 &&
          localStorage.getItem('refresh_token') &&
          !req.url.includes('token/refresh')
        ) {
          console.log('Intentando refrescar el token...');
          return this.http.post<any>(`${API_BASE_URL}token/refresh/`, {
            refresh: localStorage.getItem('refresh_token')
          }).pipe(
            switchMap((data) => {
              localStorage.setItem('access_token', data.access);
              const retryReq = req.clone({
                setHeaders: { Authorization: `Bearer ${data.access}` }
              });
              return next.handle(retryReq);
            }),
            catchError((refreshError) => {
              // Si el refresh falla, elimina los tokens y redirige al login
              localStorage.removeItem('access_token');
              localStorage.removeItem('refresh_token');
              window.location.href = '/login'; // O la ruta de tu login
              return throwError(() => refreshError);
            })
          );
        }
        return throwError(() => error);
      })
    );
  }
}
