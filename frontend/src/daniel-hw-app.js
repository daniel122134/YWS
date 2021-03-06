import {html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";
import state, {PAGES} from "./state.js"
import "./tree-node.js"
import "./components/x-button.js"
import "./components/text-input.js"
import "./components/x-switch.js"
import "./components/x-icon.js"
import "./home-page.js"
import "./closet-page.js"
import "./dress.js"
import "./explore.js"
import "./item.js"
import "./contact-page.js"
import "./splash-page.js"
import "./camera-page.js"
import {openModal} from "./components/x-modal.js";

let modal = null

customElements.define("daniel-hw-app", class extends YoffeeElement {
    constructor() {
        let urlParams = new URLSearchParams(window.location.search);
        let page = urlParams.get("page");

        super({
            currentPage: page || PAGES.home,
            inSplashPage: true,
            displayContent: false
        })
    }

    open_modal(){

        let modal = openModal(
            html()`
                <style>
                    #container {
                        padding: 20px 20px;
                    }
    
                    text-input {
                        margin-left: auto;
                        background-color: #d0d0d0;
                        color:black;
                    }
                    
                    .input-with-name {
                        display: flex;
                        margin: 5px 10px;
                        align-items: center;
                    }
                    
                    .input-with-name > x-button {
                        margin-right: 5px;
                        margin-left: 5px;
                    }
                    
                    #finish-button {
                        margin-top: 20px;
                    }
                    
                    .title {
                        font-size: 18px;
                        margin: 30px 0 12px 0;
                    }
                </style>
                <div id="container">
                    <div style="font-size: 24px">Add New Item to Your Wardrobe</div>
                    
                    
                    
                    
                    <div class="desc">Item Name:</div>
                    <text-input id="item-name"></text-input>
                    <div class="margin"></div>
                    
                    <div class="desc">Size:</div>
                    <text-input id="size"></text-input>
                    <div class="margin"></div>

                    <div class="desc">Color:</div>
                    <text-input id="color"></text-input>
                    <div class="margin"></div>

                    
                    <div class="desc">Image:</div>                    
                    <input type="file" id="myfile" name="myfile">
                    <div class="margin"></div>
                    
                    <x-button id="finish-button"
                              onclick=${() => modal.close()}>
                        Cancel
                    </x-button>
                    <x-button id="finish-button"
                              onclick=${() => () => this.validateAndSend()}>
                        Save
                    </x-button>
                </div>`
        )
        return modal;
    }
    validateAndSend() {

        let item = modal.querySelector("#item-name").getValue()
        let color = modal.querySelector("#color").getValue()
        let size = modal.querySelector("#size").getValue()
        let file = modal.querySelector("#myfile")

        var reader = new FileReader();
        reader.readAsDataURL(file.files[0]);

        reader.onload = function () {
            debugger
            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({color:color,size:size, isDark:"", brand:"", image:reader.result, bodyArea:"", weather:"", isSport:"", isBusiness:"", category:item})
            } ;
            fetch('/addItem', requestOptions)
                .then(response => response.json())
                .then(data => {
                    alert(data)
                    console.log(data)});

        };


    }


    render() {
        return html(this.props, this.state, state.tree, state)`
<style>
    :host {
        display: flex;
        flex-direction: column;
        height: inherit;
        overflow-x: hidden;
    }
    .add{
        flex:1;
        border: solid;
        padding: 10px;
        border-radius: 10px;
    }
    #container {
        opacity: 0;
    }
    
    #header {
        width: -webkit-fill-available;
        display: flex;
        padding: 10px 21px;
        align-items: center;
        max-height: 44px;
        box-shadow: 0px 0px 3px 0px var(--shadow-color);
        user-select: none; 
    }
    
    #logo {
        display: flex;
        width: 36px;
        height: 36px;
        cursor: pointer;
    }
    
    #title {
        font-size: 22px;
        padding-left: 10px;
        cursor: pointer;
    }
    
    #header > .header-button {
        transition: 300ms;
        color: var(--text-color);
        cursor: pointer;
        padding: 19px 10px;
        margin: 0px 10px;
        font-size: 18px;
        border-bottom: 3px solid #00000000;
    }
    
    #header > .header-button[highlight] {
        border-bottom-color: var(--secondary-color);
        color: var(--secondary-color);
    }
    
    #header > .header-button:hover {
        transition: 300ms;
        color: var(--secondary-color);
    }
    
    #vote-button {
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }
    
    #about-button {
        margin-left: auto !important;
    }
    
    #github-button {
        display: flex;
    }
    
    #github-button > x-icon {
        margin-left: 7px;
    }
    
    #dark-theme-toggle {
        --circle-size: 20px;
    }
    
    #slide-menu-button {
        display: none;
    }
    
    @media (max-width: 800px) {
        #header {
            max-height: 26px;
        }
        
        #header > .header-button {
            font-size: 14px;
            padding: 13px 10px;
        }
        
        #github-button, #title {
            display: none;
        }
    }
    
    camera-page {
        opacity: 0;
    }
</style>

${() => this.state.displayContent && html()`
<style>
    camera-page {
        opacity: 1;
        transition: 1000ms;
    }
</style>
`}

${() => this.state.displayContent && this.state.finishedCameraStage && html()`
<style>
    #container {
        opacity: 1;
        transition: 1000ms;
    }
</style>
`}

<style>
    @media (max-width: 800px) {
        #logo {
            margin-left: ${() => this.state.currentPage === PAGES.about ? "20px" : "0"};
            margin-right: 10px;
            width: 28px;
            height: 28px;
        }
        
        #slide-menu-button {
            display: ${() => this.state.currentPage === PAGES.about ? "flex" : "none"};
        }
    }
</style>

${() => this.state.inSplashPage && html()`
<splash-page onfinish=${() => this.state.inSplashPage = false}
             onstartfinish=${() => this.state.displayContent = true}
             onstartcamera=${() => this.shadowRoot.querySelector("camera-page").startCamera()}></splash-page>
`}

${() => !this.state.finishedCameraStage && html()`
<camera-page onfinish=${() => {
            console.log("Finished")
            this.state.finishedCameraStage = true
            // this.state.displayContent = true
            this.state.inSplashPage = false
        }}></camera-page>
`}


<div id="container">
    <div id="header">
        <x-icon id="slide-menu-button" icon="fas fa-bars"
                onclick=${() => () => state.sideMenuOpen = !state.sideMenuOpen}></x-icon>
        <img id="logo" src="res/hackru.jpg" onclick=${() => () => this.switchPage(PAGES.home)} />
        <div id="title" onclick=${() => () => this.switchPage(PAGES.home)}>YWS</div>
        
        
        
        <div id="about-button" class="header-button" 
             highlight=${() => this.state.currentPage === PAGES.closet}
             onclick=${() => () => this.switchPage(PAGES.closet)}>
            Dress
        </div>
            
            
       
        
        <div id="vote-button" class="header-button" 
             highlight=${() => this.state.currentPage === PAGES.explore}
             onclick=${() => () => this.switchPage(PAGES.explore)}>
            Explore             
        </div>
        
         <div id="vote-button" class="header-button" 
             highlight=${() => this.state.currentPage === PAGES.dress}
             onclick=${() => () => this.switchPage(PAGES.dress)}>
            My Wardrobe 
        </div>
        
        <div class="margin"></div>
    <div>
                <img id="barbot" class="add" src="res/add_cloth.png" onclick=${() => modal=this.open_modal() } />
    </div>
    <div class="margin"></div>
        
        <x-switch id="dark-theme-toggle" 
                  value=${() => state.darkTheme}
                  switched=${() => () => {
            state.darkTheme = !state.darkTheme;
            document.body.setAttribute("theme", state.darkTheme ? "dark" : "light")
        }}></x-switch>
    </div>

    ${() => {
            if (this.state.currentPage === PAGES.home) {
                return html()`<home-page getstarted=${() => () => this.switchPage(PAGES.closet)} ></home-page>`
            } else if (this.state.currentPage === PAGES.closet) {
                return html()`<closet-page></closet-page>`
            } else if (this.state.currentPage === PAGES.explore) {
                return html()`<explore-page></explore-page>`
            } else if (this.state.currentPage === PAGES.dress) {
                return html()`<dress-page></dress-page>`
            }
        }}
</div>

`
    }

    switchPage(page) {
        window.history.replaceState(null, null, `?page=${page}`);
        this.state.currentPage = page;
    }
});