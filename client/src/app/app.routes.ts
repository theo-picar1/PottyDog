import { Dashboard } from './dashboard/dashboard.component';
import { DevicePage } from './device/device.component';
import { LoginPage } from './auth/login/login.component';
import { AdminLogin } from './auth/admin-login/admin-login';
import { AdminDashboard } from './admin/admin-dashboard/admin-dashboard';
import { Routes } from '@angular/router';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  {
    path: '',
    component: LoginPage
  },
  {
    path: 'admin-login',
    component: AdminLogin
  },
  {
    path: 'dashboard',
    component: Dashboard,
    canActivate: [authGuard]
  },
  {
    path: 'admin-dashboard',
    component: AdminDashboard
  },
  {
    path: 'device/:id',
    component: DevicePage,
    canActivate: [authGuard]
  }
];