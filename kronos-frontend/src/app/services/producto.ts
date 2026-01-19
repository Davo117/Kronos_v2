import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProductoService {
  
  private apiUrl = 'http://localhost:5000/api';
  private http = inject(HttpClient);

  // Obtener lista de productos
  getProductos(clienteId?: number): Observable<any[]> {
    let url = `${this.apiUrl}/productos`;
    
    if (clienteId) {
      url += `?cliente_id=${clienteId}`;
    }
    
    return this.http.get<any[]>(url);
  }

  crearProducto(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/productos`, data);
  }
}