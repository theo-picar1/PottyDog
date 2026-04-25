import { Component, signal, inject, OnInit } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";
import { dashboardData, Device } from "../../data/dashboardData";
import { DeviceCard } from "./device-card/device-card.component";
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PdSpinner } from "../components/pd-spinner/pd-spinner.component";
import { CommonModule } from "@angular/common";
import { AddDeviceDialog } from "../components/dialogs/device-settings-dialogs/add-device-dialog/add-device.component";
import { MatDialog } from "@angular/material/dialog";
import { MatMenuModule } from "@angular/material/menu";
import { Router } from "@angular/router";
import { PdDialog } from "../components/dialogs/pd-dialog/pd-dialog.component";

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
  constructor(private readonly router: Router) {}

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
      this.devices.set(dashboardData.devices);
      this.isLoading.set(false);
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