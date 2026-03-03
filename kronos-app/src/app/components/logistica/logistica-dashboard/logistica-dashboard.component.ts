import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-logistica-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './logistica-dashboard.component.html',
  styleUrl: './logistica-dashboard.component.scss'
})
export class LogisticaDashboardComponent {
  // Simulación de datos que vendrán de la API de Python
  ordenesSeleccionada: any = null;
  
  ordenes = [
    { id: 'OC-2024-001', cliente: 'Nombre del Cliente S.A', sucursal: 'Planta Norte', entrega: '2026-02-25', status: 'Sin Diseño', urgente: false },
    { id: 'OC-2024-002', cliente: 'Cliente Ejemplo 2', sucursal: 'Matriz', entrega: '2026-03-01', status: 'En Producción', urgente: true }
  ];

  seleccionarOrden(orden: any) {
    this.ordenesSeleccionada = orden;
  }

  nuevaOrden() {
    this.ordenesSeleccionada = { id: 'NUEVA', cliente: '', sucursal: '', entrega: '', status: 'Borrador' };
  }
}