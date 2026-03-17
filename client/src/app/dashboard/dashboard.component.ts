import { Component, signal } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";
import { dashboardData, Device } from "../../data/dashboardData";
import { DeviceCard } from "./device-card/device-card.component";
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { PdSpinner } from "../components/pd-spinner/pd-spinner.component";
import { CommonModule } from "@angular/common";

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

export class Dashboard {
  devices = signal<Device[]>([]);
  isLoading = signal<boolean>(true);

  ngOnInit() {
    setTimeout(() => {
      this.devices.set(dashboardData.devices);
      this.isLoading.set(false);
    }, 1500);
  }

  trackById(index: number, device: Device) {
    return device.id
  }
}