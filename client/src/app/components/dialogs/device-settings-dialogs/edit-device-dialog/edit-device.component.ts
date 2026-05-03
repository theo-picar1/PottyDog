import { Component, OnInit, Inject, signal } from "@angular/core";
import { MatDialogContent, MatDialogActions, MatDialogTitle, MatDialogClose, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { AbstractControl, FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { HttpClient } from "@angular/common/http";

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
	constructor(
		private readonly formBuilder: FormBuilder,
		@Inject(MAT_DIALOG_DATA) public data: any,
		private readonly http: HttpClient
	) { }

	submitted: boolean = false;
	editDeviceForm: FormGroup = new FormGroup({
		deviceName: new FormControl(''),
		deviceLocation: new FormControl('')
	});

	ngOnInit() {
		this.editDeviceForm = this.formBuilder.group({
			deviceName: [this.data.deviceName, [
				Validators.required,
				Validators.minLength(2),
				Validators.maxLength(25)
			]],
			deviceLocation: [this.data.deviceLocation, [
				Validators.required
			]]
		})
	}

	get formControls(): { [key: string]: AbstractControl } {
		return this.editDeviceForm.controls;
	}

	onSubmit() {
		console.log("Submit test");
	}
}