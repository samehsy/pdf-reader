import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
// import { ColorSketchModule } from 'ngx-color/sketch';
import { ColorTwitterModule } from 'ngx-color/twitter'; // <color-twitter></color-twitter>
import { MatMenuModule } from '@angular/material/menu';
import { ColorSelectorComponent } from './color-selector/color-selector.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSliderModule } from '@angular/material/slider';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { PdfViewerModule } from 'ng2-pdf-viewer';
import { CanvasComponent } from './canvas/canvas.component';
import { VedioStreamComponent } from './vedio-stream/vedio-stream.component';
import { SocketIoModule, SocketIoConfig } from 'ngx-socket-io';
import { environment } from 'src/environments/environment';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';

const config: SocketIoConfig = {
  url: environment.baseUrl, // socket server url;
   
};

@NgModule({
  declarations: [
    AppComponent,
    ColorSelectorComponent,
    CanvasComponent,
    VedioStreamComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatIconModule,
    MatButtonModule,
    SocketIoModule.forRoot(config),

    // ColorSketchModule,
    ColorTwitterModule,
    MatMenuModule,
    MatToolbarModule,
    MatSliderModule,
    MatProgressBarModule,
    PdfViewerModule,
    MatSlideToggleModule
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
