import {
  ChangeDetectorRef,
  Component,
  ElementRef,
  OnInit,
  ViewChild,
} from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CoreService } from './core.service';
import { ColorEvent } from 'ngx-color';
import { MatSliderChange } from '@angular/material/slider';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { HttpHeaders } from '@angular/common/http';
import html2canvas from 'html2canvas';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  @ViewChild('screen')
  screen!: ElementRef;
  @ViewChild('canvas')
  canvas!: ElementRef;
  @ViewChild('downloadLink')
  downloadLink!: ElementRef;

  prevOP :any =  { down : true};

  @ViewChild('pager')
  pager!: ElementRef<HTMLButtonElement>;

  dataLocalUrl!: any;
  base64data: any;
  fileName = '';
  loading = false;
  zIndex = 0;
  activeEyeTracking = false;
  pageVariable = 0;

  constructor(
    private sanitizer: DomSanitizer,
    private service: CoreService,
    private cd: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.scrollEvent();
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.fileName = file.name;
      let formData = new FormData();
      formData.append('pdf', file);
      this.service.proccessPDF(formData).subscribe(async (data: any) => {
        var newBlob = new Blob([data], { type: 'application/pdf' });
        this.dataLocalUrl = await newBlob.arrayBuffer();
      });
    }
  }

  changeTextColor(event: ColorEvent) {
    let rgba = event.color.rgb;
    this.loading = true;
    this.service.changeTextColor(rgba).subscribe(async (data: any) => {
      var newB = new Blob([data], { type: 'application/pdf' });
      this.dataLocalUrl = await newB.arrayBuffer();
      this.loading = false;
    });
  }

  changeBackgroundColor(event: ColorEvent) {
    let rgba = event.color.rgb;
    this.loading = true;
    this.service.changeBackgroundColor(rgba).subscribe(async (data: any) => {
      var newB = new Blob([data], { type: 'application/pdf' });
      this.dataLocalUrl = await newB.arrayBuffer();
      this.loading = false;
    });
  }

  changeEyeComfort(event: MatSliderChange) {
    let rgba = { r: 0, g: 0, b: event.value, a: 0 };
    this.loading = true;
    this.service.changeEyeComfort(rgba).subscribe(async (data: any) => {
      var newB = new Blob([data], { type: 'application/pdf' });
      this.dataLocalUrl = await newB.arrayBuffer();
      this.loading = false;
    });
  }

  eyeTracking() {
    this.activeEyeTracking = !this.activeEyeTracking;
    this.service.activeEyeTracking(this.activeEyeTracking).subscribe((data) => {
      console.log(data);
    });
  }
  formatLabel(value: number) {
    if (value >= 1000) {
      return Math.round(value / 1000) + 'k';
    }

    return value;
  }

  public onClick() {
    const textLayer = document.getElementsByClassName('textLayer');
    let select = window.getSelection();
    if (select && select.rangeCount && textLayer.length > 0) {
      console.log(select);

      const x =
        select.getRangeAt(0).getClientRects()[0]?.left -
        textLayer[0].getBoundingClientRect()?.left;
      const y =
        select.getRangeAt(0).getClientRects()[0]?.top -
        textLayer[0].getBoundingClientRect()?.top;
      console.log(x, y);
    }
  }

  darkMode(e: MatSlideToggleChange) {
    this.loading = true;
    this.service.darkMode(e.checked).subscribe(async (data: any) => {
      var newB = new Blob([data], { type: 'application/pdf' });
      this.dataLocalUrl = await newB.arrayBuffer();
      this.loading = false;
    });
  }

  setHighlight(e: any) {
    // console.log(this.pageVariable);
    console.log(e);
    let options = {
      ...e,
      page: this.pageVariable,
    };
    this.loading = true;
    this.service.setHightLight(options).subscribe(async (data: any) => {
      var newB = new Blob([data], { type: 'application/pdf' });
      this.dataLocalUrl = await newB.arrayBuffer();
      this.loading = false;
    });
  }

  scrollPdf(e: any) {
    // console.log(e);
  }

  scrollEvent() {
    this.service.onScrollEvent().subscribe((data: any) => {
      setTimeout(() => {
        let pages = document.querySelectorAll('div[data-page-number]');
        console.log(data);
        
        if (data['up'] && this.prevOP['up'] != data['up']) {
          this.pageVariable -= 1;
        }
        if (data['down'] && this.prevOP['down'] != data['down']) {
          this.pageVariable += 1;
        }
        if (data['screenshot'] && this.prevOP['screenshot'] != data['screenshot']) {
          this.downloadImage();
        }

        this.prevOP = data;
        pages[this.pageVariable].scrollIntoView();
      }, 4000);
    });
  }

  downloadImage() {
    html2canvas(this.screen.nativeElement).then((canvas) => {
      this.canvas.nativeElement.src = canvas.toDataURL();
      this.downloadLink.nativeElement.href = canvas.toDataURL('image/png');
      this.downloadLink.nativeElement.download = 'marble-diagram.png';
      this.downloadLink.nativeElement.click();
    });
  }
}
