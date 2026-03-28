import { Component, Input } from "@angular/core";
import { MatIconModule } from "@angular/material/icon";

@Component({
  selector: 'pd-button',
  templateUrl: './pd-button.component.html',
  styleUrl: './pd-button.component.scss',
  imports: [MatIconModule]
})

export class PdButton {
  @Input() text!: string;
  @Input() icon?: string = "";
  @Input() labelType?: 'before' | 'after';
}