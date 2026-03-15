import { Component } from "@angular/core";
import { Header } from "../components/header/header.component";
import { Footer } from "../components/footer/footer.component";

@Component({
  selector: 'landing-page',
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.scss',
  imports: [Header, Footer]
})

export class LandingPage {}