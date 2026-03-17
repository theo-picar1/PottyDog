import { Component, Input } from "@angular/core";
import { Device } from "../../../data/dashboardData";
import { RouterLink } from "@angular/router";

@Component({
  selector: 'device-card',
  templateUrl: './device-card.component.html',
  styleUrl: './device-card.component.scss',
  imports: [RouterLink]
})

export class DeviceCard {
  @Input() device!: Device;
}