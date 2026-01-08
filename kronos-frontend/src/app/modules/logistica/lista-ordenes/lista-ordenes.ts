import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { LogisticaService } from '../../../services/logistica';

@Component({
  selector: 'app-lista-ordenes',
  standalone: true,
  imports: [CommonModule, RouterLink], 
  templateUrl: './lista-ordenes.html',
  styleUrl: './lista-ordenes.scss'
})
export class ListaOrdenes implements OnInit {

  private logisticaService = inject(LogisticaService);
  
  listaPedidos: any[] = [];
  cargando: boolean = true;

  ngOnInit(): void {
    this.cargarPedidos();
  }

  cargarPedidos() {
    this.cargando = true;
    this.logisticaService.getPedidos().subscribe({
      next: (data) => {
        this.listaPedidos = data;
        this.cargando = false;
      },
      error: (err) => {
        console.error(err);
        this.cargando = false;
      }
    });
  }

  cancelarOrden(id: number) {
    if (confirm('¿Estás seguro de que deseas cancelar esta orden? Esta acción no se puede deshacer.')) {
      this.logisticaService.cancelarPedido(id).subscribe({
        next: () => {
          alert('Orden cancelada.');
          this.cargarPedidos(); // Recargamos la tabla para ver el cambio
        },
        error: (err) => alert('Error al cancelar: ' + err.message)
      });
    }
  }

  getColorEstatus(estatus: string): string {
    switch (estatus) {
      case 'CONFIRMADO': return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
      case 'PRODUCCION': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
      case 'TERMINADO': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
      case 'CANCELADO': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'; // <--- NUEVO
      default: return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  }
}