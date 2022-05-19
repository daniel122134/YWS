import {createYoffeeElement, html, YoffeeElement} from "../libs/yoffee/yoffee.min.js";

createYoffeeElement("item-page", class extends YoffeeElement {


    render() {
        return html(this.state, this.props)`
<style>
    
    #title {
        padding-bottom: 15px;
    }

    div.gallery {
      margin: 5px;
      border: 1px solid #ccc;
      float: left;
      width: 180px;
    }
    
    div.gallery:hover {
      border: 1px solid #777;
    }
    
    div.gallery img {
      width: 100%;
      height: auto;
    }
    
    div.desc {
      padding: 15px;
      text-align: center;
    }
    
    
</style>
 <!-- Image --> 
<div class="gallery">
  <a target="_blank" href=${() => "res/hackru.jpg"}>
    <img src=${() => "res/hackru.jpg"} alt="Cinque Terre" width="600" height="400">
  </a>
  <div class="desc">Add a description of the image here</div>
</div>


`
    }
});