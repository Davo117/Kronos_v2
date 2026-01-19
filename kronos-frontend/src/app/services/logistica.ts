import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LogisticaService {
  
  
  private apiUrl = 'http://localhost:5000/api';
  private http = inject(HttpClient);

  constructor() { }

  //1.Obtener Clientes
  getClientes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/clientes`);
  }

  //2.Obtener Catálogo de Productos
  getProductos(clienteId: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/productos-catalogo?cliente_id=${clienteId}`);
  }

  //3.Guardar el Pedido Completo
  guardarPedido(pedido: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/pedidos`, pedido);
  }

  //4.Obtener lista de pedidos
  getPedidos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pedidos`);
  }

  //5.Obtener pedido por ID (Para editar)
  getPedidoPorId(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/pedidos/${id}`);
  }

  // 6. Cancelar Pedido
  cancelarPedido(id: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/pedidos/${id}/cancelar`, {});
  }

  // 7. Actualizar Pedido Existente
  actualizarPedido(id: number, pedido: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/pedidos/${id}`, pedido);
  }

}