import { Component, Input } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";

@Component({
    selector: 'camera-view',
    templateUrl: './camera-view.component.html',
    styleUrl: './camera-view.component.scss',
    imports: [MatIconModule]
})

export class CameraView {
    @Input() hasCamera!: boolean;
    @Input() isOffline!: boolean;
    @Input() width: string = '100%';
    @Input() height: string = '200px';
}