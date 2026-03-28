import { Component, signal, OnInit } from "@angular/core";
import { Device, dashboardData } from "../../../data/dashboardData";
import { ActivatedRoute, RouterLink } from "@angular/router";
import { CommonModule } from "@angular/common";
import { MatIconModule } from "@angular/material/icon";
import { MatSlideToggleModule } from "@angular/material/slide-toggle";
import { PdSpinner } from "../../components/pd-spinner/pd-spinner.component";
import { CameraView } from "../../components/camera-view/camera-view.component";
import { PdButton } from "../../components/pd-button/pd-button.component";

@Component({
  selector: 'device',
  templateUrl: './device.component.html',
  styleUrl: './device.component.scss',
  imports: [
    CommonModule,
    MatIconModule,
    MatSlideToggleModule,
    PdSpinner,
    RouterLink,
    CameraView,
    PdButton
  ]
})

export class DevicePage implements OnInit {
  isLoading = signal<boolean>(true);
  foundDevice = signal<boolean>(false);
  device = signal<Device>({
    id: -1,
    name: "",
    location: "",
    status: "Off",
    isOffline: true,
    hasCamera: false
  });

  constructor(private readonly route: ActivatedRoute) { }

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id') ?? '0');
    const found = dashboardData.devices.find(d => d.id === id);
    if (found) {
      this.device.set(found);
      this.foundDevice.set(true);
    };

    setTimeout(() => {
      this.isLoading.set(false);
    }, 1000);
  }
}