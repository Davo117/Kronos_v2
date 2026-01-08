import { Component, OnInit } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router'; // 👈 Importante para los links del menú
import { initFlowbite } from 'flowbite';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink], // 👈 Agregamos RouterLink aquí
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App implements OnInit {
  title = 'kronos-frontend';

  ngOnInit(): void {
    initFlowbite();
  }
}