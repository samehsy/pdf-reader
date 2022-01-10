import { Component, ElementRef, OnInit, VERSION, ViewChild } from '@angular/core';

@Component({
  selector: 'app-vedio-stream',
  templateUrl: './vedio-stream.component.html',
  styleUrls: ['./vedio-stream.component.scss']
})
export class VedioStreamComponent implements OnInit {
  title = "live-video-demo";
  @ViewChild("video")
  video!: ElementRef;
  ngVersion: string;
  streaming = false;
  error: any;
  private stream!: MediaStream;


  private constraints = {
    audio: false,
    video: true,
  };

  constructor() {
    this.ngVersion = `Angular! v${VERSION.full}`;
  }
  ngOnInit(): void {
    
  }

  ngAfterViewInit() {
  }

  initVideo(e :any) {
    this.getMediaStream()
      .then((stream) => {
        console.log(stream);
        // stream.
        this.stream = stream;
        this.streaming = true;
      })
      .catch((err) => {
        this.streaming = false;
        this.error = err.message + " (" + err.name + ":" + err.constraintName + ")";
      });
  }
  private getMediaStream(): Promise<MediaStream> {

    const video_constraints = { video: true };
    const _video = this.video.nativeElement;
    return new Promise<MediaStream>((resolve, reject) => {
      // (get the stream)
      return navigator.mediaDevices.
        getUserMedia(video_constraints)
        .then(stream => {
          (<any>window).stream = stream; // make variable available to browser console
          console.log(stream);
          stream.getVideoTracks()
            
          _video.srcObject = stream;
          // _video.src = window.URL.createObjectURL(stream);.
          _video.onloadedmetadata = function (e: any) { };
          _video.play();
          return resolve(stream);
        })
        .catch(err => reject(err));
    });
  }
}
