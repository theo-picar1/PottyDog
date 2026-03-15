import { Routes } from '@angular/router';
import { LandingPage } from './landing-page/landing-page.component';
import { Dashboard } from './dashboard/dashboard.component';

export const routes: Routes = [
  {
    path: '',
    component: LandingPage
  },
  {
    path: 'dashboard',
    component: Dashboard
  }
];