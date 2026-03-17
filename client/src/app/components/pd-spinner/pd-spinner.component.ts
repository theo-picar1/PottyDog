import { Component, Input } from "@angular/core";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";

@Component({
  selector: 'pd-spinner',
  templateUrl: './pd-spinner.component.html',
  styleUrl: './pd-spinner.component.scss',
  imports: [MatProgressSpinnerModule]
})

export class PdSpinner { 
  @Input() height: string = '90vh';
  @Input() loadTitle: string = ''
}