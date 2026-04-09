import { Component, signal, inject, OnInit } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";
import { dashboardData, Device } from "../../data/dashboardData";
import { DeviceCard } from "./device-card/device-card.component";
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PdSpinner } from "../components/pd-spinner/pd-spinner.component";
import { CommonModule } from "@angular/common";
import { AddDeviceDialog } from "../components/dialogs/device-settings-dialogs/add-device-dialog/add-device.component";
import { MatDialog } from "@angular/material/dialog";

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  imports: [
    MatIconModule,
    DeviceCard,
    MatProgressSpinnerModule,
    PdSpinner,
    CommonModule
  ]
})

export class Dashboard implements OnInit {
  devices = signal<Device[]>([]);
  isLoading = signal<boolean>(true);
  isLoadingAddDialog = signal<boolean>(false);

  readonly dialog = inject(MatDialog);

  timeout(ms: number) {
    return new Promise(res => setTimeout(res, ms));
  }

  async openDialog() {
    this.isLoadingAddDialog.set(true);
    document.getElementById("add-device-button")?.classList.add("loading");
    await this.timeout(1000);

    document.getElementById("add-device-button")?.classList.remove("loading");
    this.isLoadingAddDialog.set(false);
    this.dialog.open(AddDeviceDialog);
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
}