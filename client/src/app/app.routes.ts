import { Routes } from '@angular/router';
import { LandingPage } from './landing-page/landing-page.component';
import { Dashboard } from './dashboard/dashboard.component';
import { DevicePage } from './device/device.component';
import { LoginPage } from './auth/login/login.component';

export const routes: Routes = [
  {
    path: '',
    component: LoginPage
  },
  {
    path: 'dashboard',
    component: Dashboard
  },
  {
    path: 'device/:id',
    component: DevicePage
  }
];