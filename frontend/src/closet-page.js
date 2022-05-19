import {YoffeeElement, createYoffeeElement, html} from "../libs/yoffee/yoffee.min.js";
import state, {PAGES} from "./state.js"
import "./mark-down.js"
import {openModal} from "./components/x-modal.js";

let modal = null
createYoffeeElement("closet-page", class extends YoffeeElement {
    constructor() {
        super({})

        let urlParams = new URLSearchParams(window.location.search);
        let doc = urlParams.get("doc");
        if (doc != null) {
            loop:
            for (let category of state.tree.children) {
                if (category.name === doc) {
                    this.setPage(category)
                    break;
                }
                for (let child of category.children) {
                    if (child.name === doc) {
                        this.setPage(child)
                        break loop;
                    }
                }
            }
        }
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

                    <div class="desc">Is dark:</div>
                    <text-input id="is-dark"></text-input>
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
    render() {
        return html(this.state, state)`
<style>
    :host {
        position: relative;
        display: flex;
        flex-direction: row;
        height: inherit;
        overflow: hidden;
    }
        
    #side-menu {
        height: -webkit-fill-available;
        display: flex;
        flex-direction: column;
        width: 240px;
        min-width: 240px;
        box-shadow: 0px 3px 3px 0px var(--shadow-color);
        overflow-y: auto;
        overflow-x: hidden;
        padding-top: 30px;
        align-items: baseline;
        font-size: 14px;
    }
    .add{
        flex:1;
        border: solid;
        padding: 10px;
        border-radius: 10px;
    }
    .margin{
        flex:2
    }
    #side-menu {
        transition: 400ms;
        margin-left: -240px;
    }
    
    #side-menu[open] {
        transition: 400ms;
        margin-left: 0;
        z-index: 100;
    }
    
    #doc-content {
        width: 100%;
        transition: 400ms;
        opacity: 1;
        padding: 3% 7% 7% 7%;
        overflow-y: auto;
        display: flex;
    }
    
    #doc-content[overlayed] {
        transition: 400ms;
        opacity: 0;
    }
    
    @media (max-width: 800px) {
        #side-menu {
            position: absolute;
        }
    }
    
    #next-previous-buttons {
        display: flex;
        font-size: 13px;
        padding-top: 30px;
        justify-content: space-between;
        align-items: center;
    }
    
    #next-previous-buttons > x-button {
        box-shadow: none;
        border: none;
        color: var(--secondary-color);
    }
    
    #next-previous-buttons > #next {
        margin-left: auto;
    }
</style>

<div id="side-menu" open=${() => state.sideMenuOpen}>
    ${() => state.tree.children.map((node, index) => html()`
    <tree-node node=${() => node}
               depth=${0}>           
    </tree-node>
    `)}
</div>

<div class="margin"></div>

<div id="doc-content" overlayed=${() => state.sideMenuOpen && window.innerWidth < 800}>
    <div class="margin"></div>
    <div>
    
    <img id="barbot" class="add" src="res/add_cloth.png" onclick=${() => modal=this.open_modal() } />
    
    </div>
    <div class="margin"></div>
</div>
        `
    }

    flipPage(nextPage) {
        this.setPage(nextPage)
        window.history.replaceState(null, null, `?page=${PAGES.closet}&doc=${state.selectedNode.name}`);

        this.shadowRoot.querySelector("#doc-content").scrollTop = 0;
    }

    setPage(page) {
        state.selectedNode.isSelected = false;
        page.isSelected = true;
        state.selectedNode = page;
    }

    validateAndSend() {
     
        let item = modal.querySelector("#item-name").getValue()
        let color = modal.querySelector("#color").getValue()
        let size = modal.querySelector("#size").getValue()
        let is_dark = modal.querySelector("#is-dark").getValue()
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({_id:"123", name:item, color:color,size:size, isDark:is_dark, brand:"", picture:"", body_area:"", weather:"", is_sport:"", is_business:"", category:""})    
    } ;
        fetch('/addItem', requestOptions)
            .then(response => response.json())
            .then(data => {
                alert(data)
                console.log(data)});
    }
    
});
