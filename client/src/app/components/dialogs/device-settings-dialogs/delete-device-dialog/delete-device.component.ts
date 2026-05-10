import { Component, Inject, signal } from "@angular/core";
import { MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { HttpClient } from "@angular/common/http";
import { AuthService } from "../../../../services/auth.service";
import { Router } from "@angular/router";

@Component({
    selector: 'delete-device',
    templateUrl: './delete-device.component.html',
    styleUrl: './delete-device.component.scss',
    imports: [
        MatDialogContent,
        MatDialogActions,
        MatDialogTitle,
        MatDialogClose
    ]
})

export class DeleteDeviceDialog {
    constructor(
        private readonly http: HttpClient,
        private readonly authService: AuthService,
        private readonly router: Router,
        @Inject(MAT_DIALOG_DATA) public data: any,
        private readonly dialogRef: MatDialogRef<DeleteDeviceDialog>
    ) { }

    isDeleted = signal<boolean>(false);

    onDelete() {
        const userId = this.authService.getUserId();
        if(userId === null || !this.authService.isAuthenticated()) {
            this.authService.logout();
        }

        const deviceId = this.data.deviceId;
        this.http.delete(`http://localhost:5000/devices/${deviceId}`)
            .subscribe({
                next: () => {
                    this.isDeleted.set(true);
                    this.dialogRef.close();
                    this.router.navigate(['/dashboard'], {
                        state: {
                            isDeleted: this.isDeleted(),
                            deviceId: deviceId
                        }
                    })
                },
                error: (err) => {
                    console.log(err.message);
                }
            })
    }
}