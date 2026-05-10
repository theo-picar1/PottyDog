import { signal, Injectable } from "@angular/core";

@Injectable({
  providedIn: 'root'
})

export class NotificationService {
  message = signal<string | null>(null);

  getMessage(): string | null {
    return this.message();
  }

  setMessage(message: string): void {
    this.message.set(message);
  }

  clearMessage(): void {
    this.message.set(null);
  }
}