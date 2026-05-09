import { Injectable } from "@angular/core";
import { Router } from "@angular/router";

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  constructor(private readonly router: Router) {}

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  private decodeToken(): any | null {
    const token = this.getToken()
    if (!token) return null

    try {
      return JSON.parse(atob(token.split('.')[1]))
    } catch {
      return null
    }
  }

  getUserId(): number | null {
    const payload = this.decodeToken()
    return payload?.id ?? null
  }

  isAuthenticated(): boolean {
    const token = this.getToken();

    if (!token) {
      return false;
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const isExpired = payload.exp * 1000 < Date.now();
      if (isExpired) {
        this.logout();
        return false;
      }

      return true;
    } catch {
      this.logout();
      return false;
    }
  }

  login(token: string) {
    localStorage.setItem('token', token);
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/']);
  }
}