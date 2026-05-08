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
import { HttpClient } from "@angular/common/http";

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

  constructor(
    private readonly route: ActivatedRoute,
    private readonly http: HttpClient
  ) { }

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id') ?? '0');
    this.http.get(`http://localhost:5000/devices/${id}`)
      .subscribe({
        next: (res: any) => {
          this.device.set(res.device);
          this.foundDevice.set(true);
          setTimeout(() => {
            this.isLoading.set(false);
          }, 1000);
        },
        error: (err) => {
          console.log("Error: ", err);
        }
      });
  }

  readonly menuTrigger = viewChild.required(MatMenuTrigger);
  readonly dialog = inject(MatDialog);

  openDialog(type: 'edit' | 'delete') {
    if (type === "edit") {
      const dialogRef = this.dialog.open(EditDeviceDialog, {
        data: {
          id: this.device()?.id,
          deviceName: this.device()?.device_name,
          deviceLocation: this.device()?.device_location
        }
      });

      dialogRef.afterClosed().subscribe(res => {
        if (res?.updated) {
          this.isLoading.set(true);
          setTimeout(() => {
            this.isLoading.set(false);
          }, 1000);

          this.device.update(device => ({
            ...device,
            device_name: res.device.deviceName,
            device_location: res.device.deviceLocation
          }));
        }
      })
    } else {
      this.dialog.open(DeleteDeviceDialog, {
        width: '400px',
        data: {
          deviceId: this.device()?.id
        }
      });
    }
  }
}