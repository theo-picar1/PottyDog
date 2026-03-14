import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatIconModule } from "@angular/material/icon";
import { Header } from './components/header/header.component';
import { Footer } from './components/footer/footer.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet, 
    MatIconModule, 
    Header,
    Footer
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('client');
}
