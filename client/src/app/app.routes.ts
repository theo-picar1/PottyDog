import { LandingPage } from './landing-page/landing-page.component';
import { Dashboard } from './dashboard/dashboard.component';
import { DevicePage } from './device/device.component';
import { LoginPage } from './auth/login/login.component';

import { Routes } from '@angular/router';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  {
    path: '',
    component: LoginPage
  },
  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard]
  },
  {
    path: 'device/:id',
    component: DevicePage,
    canActivate: [authGuard]
  }
];