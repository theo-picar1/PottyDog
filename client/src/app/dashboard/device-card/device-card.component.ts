import { Component, Input } from "@angular/core";
import { RouterLink } from "@angular/router";
import { CameraView } from "../../components/camera-view/camera-view.component";
import { Device } from "../../../models/Device";

@Component({
  selector: 'device-card',
  templateUrl: './device-card.component.html',
  styleUrl: './device-card.component.scss',
  imports: [
    RouterLink,
    CameraView
  ]
})

export class DeviceCard {
  @Input() device!: Device;
}