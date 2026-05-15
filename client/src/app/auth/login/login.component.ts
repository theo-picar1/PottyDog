import { Component, ChangeDetectionStrategy, OnInit, signal } from "@angular/core";
import { AbstractControl, FormBuilder, FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from "@angular/forms";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatIconModule } from "@angular/material/icon"
import { HttpClient } from "@angular/common/http";
import { Router } from "@angular/router";
import { AuthService } from "../../services/auth.service";
import { MESSAGES } from "../../shared/constants/messages";

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
	constructor(
		private readonly formBuilder: FormBuilder,
		private readonly router: Router,
		private readonly http: HttpClient,
		private readonly authService: AuthService
	) {};

	MESSAGES = MESSAGES
	submitted: boolean = false;
	serverError = signal<string>("");
	loginForm: FormGroup = new FormGroup({
		email: new FormControl(''),
		password: new FormControl('')
	});

	ngOnInit() {
		if(this.authService.isAuthenticated()) {
			this.router.navigate(['/dashboard']);
		}

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

		this.http.post('http://localhost:5000/login', this.loginForm.value)
			.subscribe({
				next: (res: any) => {
					this.authService.login(res.token)
					this.router.navigate(['/dashboard']);
				},
				error: (err) => {
					this.router.navigate(['/error-page'], {
						state: {
							message: "Unable to login"
						}
					});
				}
			})
	}

	onReset() {
		this.submitted = false;
		this.loginForm.reset();
	}
} 