import { Component, Input } from "@angular/core";
import { Device } from "../../../data/dashboardData";

@Component({
  selector: 'device-card',
  templateUrl: './device-card.component.html',
  styleUrl: './device-card.component.scss'
})

export class DeviceCard {
  @Input() device!: Device;
}