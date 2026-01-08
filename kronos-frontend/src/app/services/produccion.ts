import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Produccion {
  
  private apiUrl = 'http://localhost:5000/api';
  private http = inject(HttpClient);

  getDashboardData(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/produccion/dashboard`);
  }
}