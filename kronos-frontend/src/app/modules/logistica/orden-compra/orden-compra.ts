import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common'; 
import { FormsModule } from '@angular/forms'; 
import { initFlowbite } from 'flowbite';
import { Logistica } from '../../../services/logistica';


interface DetalleOrden {
  productoId: string;
  cantidad: number;
  unidad: string;
  notas: string;
}

@Component({
  selector: 'app-orden-compra',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './orden-compra.html', 
  styleUrl: './orden-compra.scss' 
})

export class OrdenCompra implements OnInit {
  // 3. INYECTAMOS EL SERVICIO
  // Nota: Si tu clase en el archivo se llama 'Logistica', cambia LogisticaService por Logistica dentro del inject
  private logisticaService = inject(Logistica);

  catalogoClientes: any[] = [];
  catalogoSucursales: any[] = [];
  catalogoProductos: any[] = [];

  clienteSeleccionado: string = '';
  sucursalSeleccionada: string = '';
  noOrden: string = '';
  fechaDocumento: string = '';
  fechaRecepcion: string = '';
  fechaEntrega: string = '';

  productosEnOrden: DetalleOrden[] = [];

  ngOnInit(): void {
    initFlowbite();
    this.cargarCatalogos();
    this.agregarFila();
  }

  cargarCatalogos() {
    // 4. SOLUCIÓN ERROR TS7006: Agregamos el tipo ': any' explícito
    this.logisticaService.getClientes().subscribe((data: any) => {
      this.catalogoClientes = data;
    });

    this.logisticaService.getProductos().subscribe((data: any) => {
      this.catalogoProductos = data;
    });
  }

  onClienteChange() {
    this.catalogoSucursales = [];
    this.sucursalSeleccionada = '';
    
    // Convertimos a string ambos para comparar sin problemas de tipos
    const cliente = this.catalogoClientes.find((c: any) => c.id == this.clienteSeleccionado);
    
    if (cliente && cliente.sucursales) {
      this.catalogoSucursales = cliente.sucursales;
    }
  }

  agregarFila() {
    this.productosEnOrden.push({
      productoId: '', 
      cantidad: 0,
      unidad: '',
      notas: ''
    });
  }

  eliminarFila(index: number) {
    if (this.productosEnOrden.length > 1) {
      this.productosEnOrden.splice(index, 1);
    } else {
      alert("La orden debe tener al menos un producto.");
    }
  }

  actualizarUnidad(index: number) {
    // Lógica futura para unidad
  }

  guardarOrden() {
    if (!this.clienteSeleccionado) {
      alert("Selecciona un cliente");
      return;
    }

    const payload = {
      cliente_id: this.clienteSeleccionado,
      sucursal_id: this.sucursalSeleccionada,
      numero_orden_cliente: this.noOrden,
      fecha_documento: this.fechaDocumento,
      fecha_recepcion: this.fechaRecepcion,
      fecha_entrega_pactada: this.fechaEntrega,
      productos: this.productosEnOrden
    };

    console.log("Enviando...", payload);

    this.logisticaService.guardarPedido(payload).subscribe({
      // 5. SOLUCIÓN ERROR TS7006: Tipos explícitos aquí también
      next: (resp: any) => {
        alert("¡Orden guardada con éxito! ID: " + resp.id);
        // Opcional: Reiniciar formulario
        this.productosEnOrden = [];
        this.agregarFila();
      },
      error: (err: any) => {
        console.error(err);
        alert("Error al guardar: " + (err.error?.error || err.message));
      }
    });
  }
}