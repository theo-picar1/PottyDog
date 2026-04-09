import { Component, ChangeDetectionStrategy, OnInit } from "@angular/core";
import { AbstractControl, FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatIconModule } from "@angular/material/icon"
import { Router } from "@angular/router";

@Component({
	selector: 'login',
	templateUrl: './login.component.html',
	styleUrl: './login.component.scss',
	imports: [
		MatFormFieldModule,
		MatInputModule,
		FormsModule,
		ReactiveFormsModule,
		MatIconModule
	],
	changeDetection: ChangeDetectionStrategy.OnPush,
})

export class LoginPage implements OnInit {
	submitted: boolean = false;
	loginForm: FormGroup = new FormGroup({
		email: new FormControl(''),
		password: new FormControl('')
	});

	constructor(
		private readonly formBuilder: FormBuilder,
		private readonly router: Router
	) {};

	ngOnInit() {
		this.loginForm = this.formBuilder.group({
			email: ['', [
				Validators.required,
				Validators.email
			]],
			password: ['', [
				Validators.required,
				Validators.minLength(6),
				Validators.maxLength(20)
			]]
		});
	}

	get formControls(): {
		[key: string]: AbstractControl
	} {
		return this.loginForm.controls;
	}

	onSubmit() {
		this.submitted = true;
		if(this.loginForm.invalid) return;
		
		this.router.navigate(['/dashboard']);
	}

	onReset() {
		this.submitted = false;
		this.loginForm.reset();
	}
} 