import { ChangeDetectionStrategy, Component, signal, OnInit, viewChild, inject } from "@angular/core";
import { dashboardData } from "../../data/dashboardData";
import { ActivatedRoute, RouterLink } from "@angular/router";
import { CommonModule } from "@angular/common";
import { MatIconModule } from "@angular/material/icon";
import { MatSlideToggleModule } from "@angular/material/slide-toggle";
import { PdSpinner } from "../components/pd-spinner/pd-spinner.component";
import { CameraView } from "../components/camera-view/camera-view.component";
import { MatMenuTrigger, MatMenuModule } from "@angular/material/menu";
import { MatDialog } from "@angular/material/dialog";
import { EditDeviceDialog } from "../components/dialogs/device-settings-dialogs/edit-device-dialog/edit-device.component";
import { DeleteDeviceDialog } from "../components/dialogs/device-settings-dialogs/delete-device-dialog/delete-device.component";
import { Device } from "../../models/Device";

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
    MatMenuModule
  ],
  changeDetection: ChangeDetectionStrategy.OnPush
})

export class DevicePage implements OnInit {
  isLoading = signal<boolean>(true);
  foundDevice = signal<boolean>(false);
  device = signal<Device>({
    id: -1,
    user_id: 1,
    device_name: "",
    device_location: "",
    status: "offline",
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

  readonly menuTrigger = viewChild.required(MatMenuTrigger);
  readonly dialog = inject(MatDialog);

  openDialog(type: 'edit' | 'delete') {
    if(type === "edit") {
      this.dialog.open(EditDeviceDialog, {
        data: { 
          deviceName: this.device().device_name,
          deviceLocation: this.device().device_location
        }
      });
    } else {
      this.dialog.open(DeleteDeviceDialog, {
        width: '400px',
        data: {
          deviceId: this.device().id
        }
      });
    }
  }
}