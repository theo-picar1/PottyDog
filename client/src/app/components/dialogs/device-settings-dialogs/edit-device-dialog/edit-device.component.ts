import { Component, OnInit } from "@angular/core";
import { MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose } from "@angular/material/dialog";
import { AbstractControl, FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { DeviceService } from "../../../../device/device.service";

@Component({
	selector: 'edit-device-dialog',
	templateUrl: './edit-device.component.html',
	styleUrl: './edit-device.component.scss',
	imports: [
		MatDialogContent,
		MatDialogActions,
		MatDialogTitle,
		FormsModule,
		ReactiveFormsModule,
		MatFormFieldModule,
		MatInputModule,
		MatDialogClose
	]
})

export class EditDeviceDialog implements OnInit {
	submitted: boolean = false;
	editDeviceForm: FormGroup = new FormGroup({
		deviceName: new FormControl(''),
		location: new FormControl('')
	});

	constructor(private readonly formBuilder: FormBuilder) { }

	ngOnInit() {
		this.editDeviceForm = this.formBuilder.group({
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
		return this.editDeviceForm.controls;
	}

	onSubmit() {
		console.log("Submit test");
	}
}