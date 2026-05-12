import { Component, ChangeDetectionStrategy, OnInit } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";
import { MatDialogActions, MatDialogClose, MatDialogContent, MatDialogTitle, } from '@angular/material/dialog';
import { AbstractControl, FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from "@angular/material/form-field";
import { Router } from "@angular/router";
import { MatInputModule } from "@angular/material/input";
import { MESSAGES } from "../../../../shared/constants/messages";

@Component({
	selector: 'add-device-dialog',
	styleUrl: './add-device.component.scss',
	templateUrl: './add-device.component.html',
	imports: [
		MatIconModule,
		MatDialogTitle,
		MatDialogActions,
		MatDialogClose,
		MatFormFieldModule,
		FormsModule,
		ReactiveFormsModule,
		MatInputModule,
		MatDialogContent
	],
	changeDetection: ChangeDetectionStrategy.OnPush,
})

export class AddDeviceDialog implements OnInit {
	MESSAGES = MESSAGES;
	submitted: boolean = false;
	addDeviceForm: FormGroup = new FormGroup({
		deviceName: new FormControl(''),
		location: new FormControl('')
	});

	constructor(
		private readonly formBuilder: FormBuilder,
		private readonly router: Router
	) {}

	ngOnInit() {
		this.addDeviceForm = this.formBuilder.group({
			deviceName: ['', [
				Validators.required,
				Validators.minLength(2),
				Validators.maxLength(15)
			]],
			location: ['', [
				Validators.required
			]]
		})
	}

	getFormControls(): { [key: string]: AbstractControl } {
		return this.addDeviceForm.controls;
	}

	onSubmit() {
		console.log("Submit test");
	}
}