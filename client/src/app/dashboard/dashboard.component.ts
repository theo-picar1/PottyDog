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
    private readonly http: HttpClient
  ) { }

  devices = signal<Device[]>([]);
  isLoading = signal<boolean>(true);

  readonly dialog = inject(MatDialog);

  openDialog() {
    // this.dialog.open(AddDeviceDialog);
    this.dialog.open(PdDialog, {
      data: {
        type: "not-available"
      }
    });
  }

  ngOnInit() {
    setTimeout(() => {
      const token = localStorage.getItem('token');
      if (token) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const userId = payload.id;
        const params = new HttpParams().set('user_id', userId);

        this.http.get<{ devices: Device[] }>('http://localhost:5000/devices', { params })
          .subscribe((res) => {
            this.devices.set(res.devices);
            this.isLoading.set(false);
            console.log(this.devices());
          });
      }
    }, 1000);
  }

  trackById(index: number, device: Device) {
    return device.id;
  }

  logout() {
    localStorage.removeItem('token');
    this.router.navigate(['/']);
  }
}