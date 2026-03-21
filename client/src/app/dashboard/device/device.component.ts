import { Component, signal } from "@angular/core";
import { Device } from "../../../data/dashboardData";
import { ActivatedRoute, RouterLink } from "@angular/router";
import { dashboardData } from "../../../data/dashboardData";
import { CommonModule } from "@angular/common";
import { MatIconModule } from "@angular/material/icon";
import { MatSlideToggleModule } from "@angular/material/slide-toggle";
import { PdSpinner } from "../../components/pd-spinner/pd-spinner.component";

@Component({
  selector: 'device',
  templateUrl: './device.component.html',
  styleUrl: './device.component.scss',
  imports: [
    CommonModule,
    MatIconModule,
    MatSlideToggleModule,
    PdSpinner,
    RouterLink
]
})

export class DevicePage {
  device = signal<Device | null>(null);
  isLoading = signal<boolean>(true);

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    setTimeout(() => {
      const id = Number(this.route.snapshot.paramMap.get('id') ?? '0');
      const found = dashboardData.devices.find(d => d.id === id) || null;
      this.device.set(found);
      this.isLoading.set(false);
    }, 1500);
  }
}