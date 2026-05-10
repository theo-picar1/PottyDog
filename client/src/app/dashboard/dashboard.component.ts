import { Component, signal, inject, OnInit } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";
import { DeviceCard } from "./device-card/device-card.component";
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PdSpinner } from "../components/pd-spinner/pd-spinner.component";
import { CommonModule } from "@angular/common";
import { MatDialog } from "@angular/material/dialog";
import { MatMenuModule } from "@angular/material/menu";
import { Router } from "@angular/router";
import { PdDialog } from "../components/dialogs/pd-dialog/pd-dialog.component";
import { HttpClient, HttpParams } from "@angular/common/http";
import { Device } from "../../models/Device";
import { AuthService } from "../services/auth.service";
import { MatSnackBar } from "@angular/material/snack-bar";
import { NotificationService } from "../services/notification.service";

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  imports: [
    MatIconModule,
    DeviceCard,
    MatProgressSpinnerModule,
    PdSpinner,
    CommonModule,
    MatMenuModule
  ]
})

export class Dashboard implements OnInit {
  constructor(
    private readonly router: Router,
    private readonly http: HttpClient,
    private readonly authService: AuthService,
    private readonly notificationService: NotificationService
  ) { }

  devices = signal<Device[]>([]);
  isLoading = signal<boolean>(true);

  readonly dialog = inject(MatDialog);
  readonly snackBar = inject(MatSnackBar)

  openDialog() {
    // this.dialog.open(AddDeviceDialog);
    this.dialog.open(PdDialog, {
      data: {
        type: "not-available"
      }
    });
  }

  ngOnInit() {
    const userId = this.authService.getUserId();
    if (!this.authService.isAuthenticated() || userId === null) {
      this.isLoading.set(false);
      this.authService.logout();
      return;
    }

    const params = new HttpParams().set('user_id', userId);
    this.http.get<{ devices: Device[] }>('http://localhost:5000/devices', { params })
      .subscribe({
        next: (res) => {
          this.devices.set(res.devices);
          this.isLoading.set(false);

          // After deletion of a device, show a snackbar
          const message = this.notificationService.getMessage();
          if (message === null) return;

          this.snackBar.open(message, 'Close', {
            duration: 3000
          });

          this.notificationService.clearMessage();
        },
        error: (err) => {
          this.isLoading.set(false);
          console.log(err);
          return;
        }
      });
  }

  trackById(index: number, device: Device) {
    return device.id;
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/']);
  }
}