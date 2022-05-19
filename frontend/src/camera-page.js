import {html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";
import "../src/components/x-icon.js"
import "../src/components/x-button.js"

customElements.define("camera-page", class extends YoffeeElement {
    constructor() {
        super({});
    }

    async startCamera() {
        const constraints = {
            video: {
                width: {
                    min: 1280,
                    ideal: 1920,
                    max: 2560,
                },
                height: {
                    min: 720,
                    ideal: 1080,
                    max: 1440,
                },
                facingMode: "user"
            },
        };


        this.video = this.shadowRoot.querySelector("#video");

        // current video stream
        let videoStream;
        this.video.play();
        //video.pause();


        // stopVideoStream();
        // constraints.video.facingMode = useFrontCamera ? "user" : "environment";

        try {
            videoStream = await navigator.mediaDevices.getUserMedia(constraints);
            this.video.srcObject = videoStream;
        } catch (err) {
            alert("Could not access the camera");
        }
    }

    render() {
        return html(this.state)`
        <style>
            :host {
                color: white;
                display: flex;
                font-size: 36px;
                align-items: center;
                justify-content: center;
                height: inherit;
                width: 100%;
                position: fixed;
                z-index: 1;
            }
            
            #loading {
                font-size: 50px;
                -webkit-animation: rotating 2s linear infinite;
                margin-top: 50px;
            }
            
            @-webkit-keyframes rotating {
               from{
                   -webkit-transform: rotate(0deg);
               }
               to{
                   -webkit-transform: rotate(360deg);
               }
            }
            
            video {
                position: fixed;
                z-index: -4;
            }
            
            #camera-button {
                border-radius: 1000px;
                width: 100px;
                height: 100px;
                min-width: 100px;
                z-index: 1;
                background-color: #ffffff50;
                padding: 0;
                box-shadow: 0 0 15px 4px #ffffff50;
                top: 70%;
                position: absolute;
            }
            
            #overlay {
                height: inherit;
                width: 100%;
                background-color: #ffffff10;
                z-index: -2;
                position: fixed;
            }
            
            #instructions {
                font-size: 18px;
                color: #ffffffbb;
                top: 10%;
                position: fixed;
            }
            
            #finish-buttons-container {
                display: flex;
                position: fixed;
                z-index: 1;
                top: 77%;
                font-size: 30px;
            }
            
            #finish-buttons-container > x-button {
                background-color: #ffffff10;
            }
            
            #continue-button {
                margin-left: 20px;
            }
        </style>
        <style>
            #canvas {
                z-index: -5;
            }
        </style>
        <div id="overlay"></div>
        <canvas id="canvas"></canvas>
        <video autoplay id="video"></video>
        
        ${() => this.state.approvePhotoStage ? 
        html()`
        <div id="finish-buttons-container">
            <x-button id="retake-button" onclick=${() => this.backToPhotoTakingBitch()}>
                Retake
            </x-button>
            <x-button id="continue-button" onclick=${() => this.props.onfinish()}>
                Continue
            </x-button>            
        </div>
        `
            :
        html()`<x-button id="camera-button" onclick=${() => this.takePhoto()}></x-button>`
        }
        <div id="instructions">Make sure your waist and shoulders are seen</div>
        `
    }

    backToPhotoTakingBitch() {
        this.video.play();
    }

    takePhoto() {
        this.video.pause();
        this.state.approvePhotoStage = true
        // const img = document.createElement("img");
        // canvas.width = video.videoWidth;
        // canvas.height = video.videoHeight;
        // canvas.getContext("2d").drawImage(video, 0, 0);
        // img.src = canvas.toDataURL("image/png");
        // screenshotsContainer.prepend(img);
    }
})