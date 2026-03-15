import { Component, signal } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";
import { dashboardData, Device } from "../../data/dashboardData";
import { DeviceCard } from "./device-card/device-card.component";

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
  imports: [MatIconModule, DeviceCard]
})

export class Dashboard {
  devices = signal<Device[]>(dashboardData.hasDevices);
  noDevices = signal<Device[]>(dashboardData.noDevices);
}