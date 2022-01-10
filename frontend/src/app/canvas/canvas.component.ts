import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  OnInit,
  Output,
  ViewChild,
} from '@angular/core';

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.scss'],
})
export class CanvasComponent implements OnInit, AfterViewInit {
  @Output() setHighlight = new EventEmitter<any>();
  @Output() scrollPdf = new EventEmitter<any>();

  // @HostListener('scroll', ['$event']) // for scroll events of the current element
  @HostListener('window:scroll', ['$event']) // for window scroll events
  onScroll(event: any): void {
    this.scrollPdf.emit(event);
  }

  @ViewChild('parent', { static: true })
  parentElm!: ElementRef<HTMLDivElement>;

  @ViewChild('div', { static: true })
  divElm!: ElementRef<HTMLDivElement>;

  div!: HTMLDivElement;
  parent!: HTMLDivElement;

  last_mousex = 0;
  last_mousey = 0;
  final_x = 0;
  final_y = 0;
  mousedown = false;

  constructor() {}

  ngOnInit(): void {}

  ngAfterViewInit(): void {
    this.div = this.divElm.nativeElement;
    this.parent = this.parentElm.nativeElement;
  }

  mouseDown(e: MouseEvent) {
    let parentPos = this.parent.getBoundingClientRect();
    let x = e.clientX - parentPos.left;
    let y = e.clientY - parentPos.top;
    this.last_mousex = x;
    this.last_mousey = y;
    this.div.style.left = x + 'px';
    this.div.style.top = y + 'px';
    this.div.style.visibility = 'visible';
    this.mousedown = true;
  }
  mouseUp(e: MouseEvent) {
    this.mousedown = false;
    setTimeout(() => {
      let parentPos = this.parent.getBoundingClientRect();

      this.final_x = e.clientX - parentPos.left;
      this.final_y = e.clientY - parentPos.top;
      this.div.style.width = 0 + 'px';
      this.div.style.height = 0 + 'px';
      this.div.style.visibility = 'hidden';
      this.getFinalPos();
    }, 500);
  }
  mouseMove(e: MouseEvent) {
    let parentPos = this.parent.getBoundingClientRect();
    let x = e.clientX - parentPos.left;
    let y = e.clientY - parentPos.top;
    if (this.mousedown) {
      this.div.style.position = 'absolute';
      if (this.last_mousex - x > 0) this.div.style.left = x + 'px';
      if (this.last_mousey - y > 0) this.div.style.top = y + 'px';
      this.div.style.width = Math.abs(this.last_mousex - x) + 'px';
      this.div.style.height = Math.abs(this.last_mousey - y) + 'px';
    }
  }

  getFinalPos() {
    let relativePos = {
      final_y:
        this.final_y > this.last_mousey ? this.final_y : this.last_mousey,

      final_x: this.final_x > this.last_mousex ? this.final_x : this.last_mousex,
      last_mousex:  this.final_x > this.last_mousex ? this.last_mousex : this.final_x,
      last_mousey:  this.final_y > this.last_mousey ? this.last_mousey : this.final_y, 
    };
    this.setHighlight.emit(relativePos);
  }
}
