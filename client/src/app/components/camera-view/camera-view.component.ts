import { Component, Input } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";
import { MESSAGES } from "../../shared/constants/messages";

@Component({
    selector: 'camera-view',
    templateUrl: './camera-view.component.html',
    styleUrl: './camera-view.component.scss',
    imports: [MatIconModule]
})

export class CameraView {
    @Input() hasCamera!: boolean;
    @Input() isOffline!: boolean;

    MESSAGES = MESSAGES;
}