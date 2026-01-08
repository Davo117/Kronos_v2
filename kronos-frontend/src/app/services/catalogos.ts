import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CatalogosService {
  
  private apiUrl = 'http://localhost:5000/api';
  private http = inject(HttpClient);

  // --- CIUDADES ---
  getCiudades(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/ciudades`);
  }

  crearCiudad(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/ciudades`, data);
  }

  // --- CLIENTES ---
  crearCliente(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/clientes-completo`, data);
  }

  // --- SUCURSALES ---
  crearSucursal(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/sucursales-completo`, data);
  }
}