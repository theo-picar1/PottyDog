import { Component, Inject, inject } from "@angular/core";
import { MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA, MatDialogRef } from "@angular/material/dialog";
import { HttpClient } from "@angular/common/http";
import { AuthService } from "../../../../services/auth.service";
import { Router } from "@angular/router";
import { NotificationService } from "../../../../services/notification.service";
import { MatSnackBar } from '@angular/material/snack-bar';
import { MESSAGES } from "../../../../shared/constants/messages";

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
        private readonly dialogRef: MatDialogRef<DeleteDeviceDialog>,
        private readonly notificationService: NotificationService
    ) { }

    private snackBar = inject(MatSnackBar);
    MESSAGES = MESSAGES;

    onDelete() {
        const userId = this.authService.getUserId();
        if (userId === null || !this.authService.isAuthenticated()) {
            this.authService.logout();
        }

        const deviceId = this.data.deviceId;
        const deviceName = this.data.deviceName;
        this.http.delete(`http://localhost:5000/devices/${deviceId}`)
            .subscribe({
                next: () => {
                    this.notificationService.setMessage(`'${deviceName}' successfully deleted!`);
                    this.dialogRef.close();
                    this.router.navigate(['/dashboard']);
                },
                error: (err) => {
                    this.notificationService.setMessage(`Device could not be deleted!`);
                    this.dialogRef.close();
                    const message = this.notificationService.getMessage();
                    if(message === null) {
                        console.log(err);
                        return;
                    };

                    this.snackBar.open(message, 'Close', {
                        duration: 3000
                    });

                    this.notificationService.clearMessage();
                }
            })
    }
}