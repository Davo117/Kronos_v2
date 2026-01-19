import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';


import { ProductoService } from '../../../services/producto'; 
import { LogisticaService } from '../../../services/logistica'; 

@Component({
  selector: 'app-gestion-productos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './gestion-productos.html',
  styleUrl: './gestion-productos.scss'
})
export class GestionProductos implements OnInit {

  private productoService = inject(ProductoService);
  private logisticaService = inject(LogisticaService);

  listaProductos: any[] = [];
  listaClientes: any[] = []; 

  nuevoProducto = {
    cliente_id: '',
    codigo: '',
    nombre: '',
    ancho: 0,
    alto: 0
  };

  mostrarFormulario = false; 

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos() {
    // Cargar Clientes
    this.logisticaService.getClientes().subscribe(data => this.listaClientes = data);
    
    // Cargar Productos usando el nuevo servicio
    this.productoService.getProductos().subscribe(data => this.listaProductos = data);
  }

  guardar() {
    this.productoService.crearProducto(this.nuevoProducto).subscribe({
      next: () => {
        alert('Diseño registrado correctamente');
        this.nuevoProducto = { cliente_id: '', codigo: '', nombre: '', ancho: 0, alto: 0 };
        this.mostrarFormulario = false;
        this.cargarDatos(); 
      },
      error: (e) => alert('Error: ' + (e.error?.error || e.message))
    });
  }
}