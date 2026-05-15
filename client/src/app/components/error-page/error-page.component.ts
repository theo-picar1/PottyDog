import { Component, signal } from "@angular/core";
import { Router } from "@angular/router";
import { PdSpinner } from "../pd-spinner/pd-spinner.component";

@Component({
  selector: 'error-page',
  templateUrl: './error-page.component.html',
  styleUrl: './error-page.component.scss',
  imports: [
    PdSpinner
  ]
})

export class ErrorPage {
  constructor(private readonly router: Router) {}

  message = signal<string | null>(null);
  isLoading = signal<boolean>(true);

  ngOnInit() {
    this.message.set(history.state.message ?? 'An error has occured');
    setTimeout(() => {
      this.isLoading.set(false);
    }, 1000);
  }
}