import { Component, Input, Inject } from "@angular/core";
import { MatDialogActions, MatDialogClose, MatDialogContent, MatDialogTitle, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'pd-dialog',
  templateUrl: './pd-dialog.component.html',
  styleUrl: './pd-dialog.component.scss',
  imports: [
    MatDialogTitle,
		MatDialogActions,
		MatDialogClose,
		MatDialogContent
  ]
})

export class PdDialog {
  constructor(@Inject(MAT_DIALOG_DATA) public data: any) { }
}