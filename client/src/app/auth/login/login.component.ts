import { Component, ChangeDetectionStrategy, OnInit, signal } from "@angular/core";
import { AbstractControl, FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatIconModule } from "@angular/material/icon"
import { HttpClient } from "@angular/common/http";
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
	serverError = signal<string>("");
	loginForm: FormGroup = new FormGroup({
		email: new FormControl(''),
		password: new FormControl('')
	});

	constructor(
		private readonly formBuilder: FormBuilder,
		private readonly router: Router,
		private readonly http: HttpClient
	) {};

	ngOnInit() {
		this.loginForm = this.formBuilder.group({
			email: ['', [
				Validators.required,
				Validators.email
			]],
			password: ['', [
				Validators.required
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
		if (this.loginForm.invalid) return;

		console.log(this.loginForm.value);

		this.http.post('http://localhost:5000/login', this.loginForm.value)
			.subscribe({
				next: (res: any) => {
					if(res.status_code === 200) {
						this.router.navigate(['/dashboard']);
					} else {
						console.log(res.message);
						this.serverError.set(res.message || "Something went wrong. Please try again later");
					}
				},
				error: (err) => {
					console.log(err);
					this.serverError.set(err.error?.message || "Something went wrong. Please try again later");
				}
			})
	}

	onReset() {
		this.submitted = false;
		this.loginForm.reset();
	}
} 