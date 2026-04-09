import { Component } from "@angular/core";
import { MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose } from "@angular/material/dialog";
import { DeviceService } from "../../../../device/device.service";

@Component({
    selector: 'delete-device',
    templateUrl: './delete-device.component.html',
    styleUrl: './delete-device.component.scss',
    imports: [MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose]
})

export class DeleteDeviceDialog {
    
}