import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class Logistica {
  
  
  private apiUrl = 'http://localhost:5000/api';
  private http = inject(HttpClient);

  constructor() { }

  // 1. Obtener Clientes
  getClientes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/clientes`);
  }

  // 2. Obtener Catálogo de Productos
  getProductos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/productos-catalogo`);
  }

  // 3. Guardar el Pedido Completo
  guardarPedido(pedido: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/pedidos`, pedido);
  }
}