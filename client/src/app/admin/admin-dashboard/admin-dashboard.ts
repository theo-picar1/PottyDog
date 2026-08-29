import { Component } from '@angular/core';
import { MESSAGES } from '../../shared/constants/messages';
import { DashboardCard } from '../../components/dashboard-card/dashboard-card';

@Component({
  selector: 'app-admin-dashboard',
  imports: [
    DashboardCard
  ],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.scss',
})
export class AdminDashboard {
  MESSAGES: any = MESSAGES;
  dashboardCards: any = [
    // Users card
    {
      title: MESSAGES.ADMIN_DASHBOARD.USER_CARD_TITLE,
      description: MESSAGES.ADMIN_DASHBOARD.USER_CARD_DESC,
      buttonText: MESSAGES.ADMIN_DASHBOARD.USER_CARD_BUTTON_TEXT
    },
    // Devices card
    {
      title: MESSAGES.ADMIN_DASHBOARD.DEVICE_CARD_TITLE,
      description: MESSAGES.ADMIN_DASHBOARD.DEVICE_CARD_DESC,
      buttonText: MESSAGES.ADMIN_DASHBOARD.DEVICE_CARD_BUTTON_TEXT
    }
  ]
}
