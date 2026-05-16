import { Component, signal } from "@angular/core";
import { Router } from "@angular/router";
import { PdSpinner } from "../pd-spinner/pd-spinner.component";
import { MESSAGES } from "../../shared/constants/messages";

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

  statusCode: number = -1;
  isLoading = signal<boolean>(true);
  messageMap: { [key: number]: string } = {
    0: MESSAGES.ERRORS.STATUS_0_ERROR,
    403: MESSAGES.ERRORS.STATUS_403_ERROR,
    500: MESSAGES.ERRORS.STATUS_500_ERROR,
    503: MESSAGES.ERRORS.STATUS_503_ERROR
  }
  errorMessage: string = "";

  ngOnInit() {
    if(!history.state.code) {
      console.error("An unknown error has occured. You will be redirected to the login page shortly.")
      this.router.navigate(['/login']);
    }

    this.statusCode = history.state.code;
    this.errorMessage = this.messageMap[this.statusCode];
    
    setTimeout(() => {
      this.isLoading.set(false);
    }, 1000);
  }
}