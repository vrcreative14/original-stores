function UpdateProductDetails() {
    debugger
    let productType = document.querySelector('#select-prodtype').value
    let tagList = []
    let list = []
    switch (productType) {
        case 'Fashion & Clothing':
            //let list = ['Shirts & T-Shirts','Trousers & Jeans','']
            //let dict = {Men : ['Shirts & T-Shirts','Trousers & Jeans','Suitings','Ethnic Wear','Wollens'], Women:['Sarees']}
            //let list = ['Product Name','Colour','Fabric','Sizes Available','Number of Pockets', , '']
            let list1 = ["Men's Wear", "Women's Wear", "Kid's Wear"]
            AddTags(list1, 'Clothing & Fashion')
            break;
        case 'Home Appliances':
            //let list = ['Television','Speakers','Air-Conditioners','Lightings','Washing-Machine','','Mixers & Grinders']
            //let list = ['Product Name','Colour','Body Material','Power Consumption','Number of Pockets', 'Adequate Seasons', '']
            let list2 = ['Air Conditioners', 'Washing Machine', 'Mixers & Grinders', 'Vaccum Cleaners', 'Room Heaters', 'Fans', 'Desert Coolers', 'Blenders', 'Others']
                //list2.concat(tagList)
            AddTags(list2, 'Home Appliances')
            break;
        case 'Fabrics & Household':
            break;
        case 'Gift Items':
            break;
        case 'Electrical tools & machinery':
            break;
        case 'Mobile Phones':
            break;
        case 'Mobile Phone Accessories':
            let list = ['Product Name', 'Colour', 'Material', 'Number of Ports', '', '', '']
            break;
        case 'Sports Items':
            break;
        case 'Footwear':
            break;
        default:
            break;
    }
}

const AddTags = (list, category) => {
    const div = document.createElement('div');
    debugger
    var elem = document.getElementById('product_details_div');
    if (elem.childElementCount > 0)
        elem.parentNode.removeChild(elem);

    div.className = 'fields';
    div.id = 'product_details'
    switch (category) {
        case 'Clothing & Fashion':
            var tag = ` <div><div class="required inline field"> <label class="formLabel">Select the type of Clothing</label>
            </div>
          `
            debugger
            list.forEach(function(item) {
                tag += `
                  <div class="ui radio checkbox" style="margin-top:10px;margin-right:25px;">
                    <input id="clothing_category" name="clothing_category" type="radio" class="subcategory" value="${item}" onclick="UpdateForm2()">
                    <label class="formLabel">${item}</label>
                    </div>                 
                 `
            });
            tag += `</div>`
            div.innerHTML = tag
            document.querySelector('#product_details_div').appendChild(div)
            break;
        case 'Home Appliances':

            var tag = ` <div><div class="required inline field"> <label class="formLabel">Select the type of Home Appliance</label>
            </div>
          `
            debugger
            list.forEach(function(item) {
                tag += `
                  <div class="ui radio checkbox" style="margin-top:10px;margin-right:25px;">
                    <input id="appliances_category" name="appliances_category" type="radio" class="subcategory" value="${item}" onclick="UpdateForm2()">
                    <label class="formLabel">${item}</label>
                    </div>                 
                 `
            });
            tag += `</div>`
            div.innerHTML = tag
            document.querySelector('#product_details_div').appendChild(div)

            break;

        case "Men's Wear":
        case "Kid's Wear":
        case "Women's Wear":
            var elem = document.getElementById('product_moredetails');
            if (elem != null)
                elem.parentNode.removeChild(elem);
            // const div = document.createElement('div');
            //div.className = ' fields';
            div.id = 'product_moredetails'
            var tag = `<label class="formLabel">Select the type of ${category} </label>`
            tag += `<div class="fields"><div class="six wide field">
            <select id="select_garment" class="ui dropdown" onchange="UpdateForm3()">`

            list.forEach(function(items) {
                let type = Object.keys(items)[0]
                tag += `<label>${type}</label>`
                    //  items.forEach(function(item){
                    //     tag+=`<option value="${item}">${item}</option>`
                    //  });
                let i = 0
                for (var key in items) {
                    for (let j = 0; j < items[key].length; j++) {
                        tag += `<option id="" value="${items[key][i]}" onchange="UpdateForm3()">${items[key][i]}</option>`
                        i++
                    }
                }
            });
            tag += `</select>
          </div></div>`
            let specs = ['Fabric Used', 'Number Of Pockets']
            specs.forEach(function(item) {
                switch (item) {
                    case 'Fabric Used':
                        tag += `
                <div id="add_fabric_div">
                <div class="fields">
                <div class="six wide field">
                <div class="required  field">                
                <label>${item}</label>  
                <span id="fabricerrorLabel" class="ui bottom pointing red basic label promptLabel">Grament Fabric is required</span>                                                                  
                </div>
                <input type="text" class="fabric">                
                </div>              
                <div class="four wide field">
                <div class="required field">
                <label>Percentage out of total</label> 
                <span id="fabricpercentageerrorLabel" class="ui bottom pointing red basic label promptLabel">Fabric % is required</span>                                                                  
                </div>   
                <input type="text" class="percentage" style="width:100px;">
                </div>
                <div class="two wide field">
                <label>Add Fabric</label>              
                <button class="small ui blue compact icon button" onclick="AddTags([],'AddFabric')">
                <i class="plus icon"></i>
                </button>
                </div>                             
               `
                        break;
                    case 'Number Of Pockets':
                        tag += `
                <div class="one wide field"></div>
                <div class="twelve wide field">
                <div class="inline field">       
                <label>${item}</label>                                
                <input type="text" value="1" text="1" id="no_of_pockets" maxlength="2" placeholder="1" onkeypress="return (event.charCode !=8 && event.charCode ==0 || (event.charCode >= 48 && event.charCode <= 57))" maxlength="10" style="width: 55px;">                          
           
               
                <button class="small ui blue compact icon button" onclick="plusminusValue('no_of_pockets','+')">
                <i class="plus icon"></i>
                </button>

                <button class="medium ui blue compact icon button" onclick="plusminusValue('no_of_pockets','-')">
                <i class="minus icon"></i>
                </button>
                </div>
                
                </div>
                </div>
                </div>`
                        break;
                }
            });
            //tag += `<button class="ui button successBtn">Save Product</button>`
            div.innerHTML = tag
            document.querySelector('#product_details_div2').appendChild(div)
            const div2 = document.createElement('div');
            div2.className = "four wide field"
            div2.id = "sizes_available"
            tag = `
          <div class="inline required field">
          <label>Sizes Available </label>
          <span id="colorserrorLabel" class="ui left pointing red basic label promptLabel">Select the sizes available</span>                                            
          </div>
          <select id="available_sizes" name="availableSizes"  multiple="" class="ui fluid dropdown">                         
              <option value="all"> All sizes available</option>    
              <option value="S">Small</option>
              <option value="M">Medium</option>
              <option value="L">Large</option>
              <option value="XL">XL</option>
              <option value="XXL">XXL</option>
              <option value="XXXL"> XXXL</option>                                                            
          </select>`
            div2.innerHTML = tag
            document.querySelector('#appearance_details').appendChild(div2)
            $('#available_sizes').dropdown()
            break;
        case 'Shirts':
            var elem = document.getElementById('garment_moredetails');
            if (elem != null)
                elem.parentNode.removeChild(elem);
            // const div = document.createElement('div');
            div.className = 'inline fields';
            div.id = 'garment_moredetails'
            var tag = ''
            list.forEach(function(item) {
                tag += `<div class="four wide field">
            <label>${item}</label>
            <div class="inline field">           
            <input type="text">
            </div>`
            });
            div.innerHTML = tag
            document.querySelector('#product_moredetails').appendChild(div)
            break;

        case 'AddFabric':
            let parentDiv = document.querySelector('#add_fabric_div')
            if (parentDiv.childElementCount >= 10) {
                break;
            }
            div.className = 'fields';
            div.id = ''
            var tag = ''
            tag += `           
            <div class="five wide field">
            <label>Fabric Used</label>                        
            <input type="text" class="fabric">                
            </div>  

            <div class="two wide field">
            <label>Percentage out of total</label>    
            <input type="text" class="percentage" style="width:100px;">
            </div>  
            <div class="four wide field">
            <label>Remove</label>
            <button class="small ui blue compact icon button" onclick="RemoveTags([],'Fabric',this)">
            <i class="minus icon"></i>
            </button>         
            `
            div.innerHTML = tag
            parentDiv.appendChild(div)
            break;
        case 'Air Conditioners':
            var elem = document.getElementById('appliance_moredetails');
            if (elem != null)
                elem.parentNode.removeChild(elem);
            // const div = document.createElement('div');
            div.className = 'inline fields';
            div.id = 'appliance_moredetails'
            var tag = ''
            list.forEach(function(item) {
                tag += `<div class="four wide field">
            <label>${item}</label>
            <div class="inline field">           
            <input type="text">
            </div>`
            });
            div.innerHTML = tag
            document.querySelector('#product_moredetails').appendChild(div)
            break;

        case 'Others':
            var tag = ''
            tag += `<div class="inline field"><div class="four wide field">
            <input type="text"/>
            </div></div>`
            div.innerHTML = tag
            document.querySelector('#product_moredetails').appendChild(div)
            break;

    }
}

const UpdateForm2 = () => {
    debugger
    //var subcategories = document.getElementsByClassName('subcategory').value
    let clothing_categories = document.getElementsByName('clothing_category')
    for (let i = 0; i < clothing_categories.length; i++) {
        if (clothing_categories[i].checked == true) {
            var clothing_category = clothing_categories[i].value
        }
    }
    let list = []
    switch (clothing_category) {
        case "Men's Wear":
            list = [
                { Shirts: ['Formal Shirts', 'Casual Shirts', 'Party Wear Shirts'] },
                { Trousers: ["Formal Trousers", "Chinos", "Jeans"] },
                { Ethnic: ["Kurta", 'Pyjama', 'Sadri', 'Kurta-Pyjama', 'Sherwani', 'Others'] },
            ]
            AddTags(list, "Men's Wear")
            break;
        case "Women's Wear":
            list = [
                { Ethnic: ['Sarees', 'Kurtas', 'Plazo', "Shawls & Dupattas"] }, { Accessories: ["Watches", "Bangles"] },
                { Casual: ['Jeans', 'Tops', 'Shirts', 'T-Shirts', 'leggings', 'Blazers', 'Jackets', 'Coats', 'Others'] },
            ]
            AddTags(list, "Women's Wear")
            break;

        case "Kid's Wear":
            list = [
                { GirlsCasual: ['T-Shirts', 'Tops', 'Dresses', 'Lowers'] },
                { BoysCasual: ['Shirts', 'Others'] },
            ]
            AddTags(list, "Kid's Wear")
            break;
        case "Blenders":
        case "Mixers & Grinders":
            break;
        case "Air Conditioners":
            list = [
                { Type: ['Window AC', 'Split AC', 'Central AC', 'Portable AC', 'Others'] },
                { Capacity: ['0.8 ton', '1.0 ton', '1.5 ton', '2.0 ton', 'Others'] },
                { EnergyRating: ['1', '2', '3', '4', '5'] },
                { EnergyConsumption: [] }
            ]
            AddTags(list, "Air Conditioners")
            break;
        case "Washing Machine":
            break;
        case "Fans":
        case "Coolers":
            break;
    }
}

const UpdateForm3 = () => {
    let selected_garment = document.getElementById('select_garment').value
    let list = []
    switch (selected_garment) {
        case "Shirts":
            list = ['Fabric', 'No of Pockets']
                //AddTags(list,'Shirts')
            break;
        case "Trousers":

            break;
        case 'Others':
            AddTags([], 'Others')
            break;
    }
    console.log('checked')
}

const RemoveTags = (list, category, elem) => {
    debugger
    switch (category) {
        case 'Fabric':
            document.querySelector('#add_fabric_div').removeChild(elem.parentNode.parentNode);
            break;
        case '':
            break;
    }
}

const plusminusValue = (elem, operation) => {
    let num = document.getElementById(elem).value
    debugger
    switch (operation) {
        case '+':
            if (elem.toString().includes("pockets") && parseInt(num) >= 99)
                break;
            num = parseInt(num) + 1
            document.getElementById(elem).value = num
            break;

        case '-':
            if (parseInt(num) <= 0)
                break;
            num = parseInt(num) - 1
            document.getElementById(elem).value = num
            break;
    }
}

function isNumberKey(txt, evt) {
    var charCode = (evt.which) ? evt.which : evt.keyCode;
    if (charCode == 46) {
        //Check if the text already contains the . character
        if (txt.value.indexOf('.') === -1) {
            return true;
        } else {
            return false;
        }
    } else {
        if (charCode > 31 &&
            (charCode < 48 || charCode > 57))
            return false;
    }
    return true;
}

function SaveProduct(category) {

    var dict = {};
    switch (category) {
        case 'Clothing':
            var inputs = document.getElementById('product_details_form').querySelectorAll('input')
            for (let i = 0; i < inputs.length; i++) {
                let element_id = inputs[i].id
                let prod = ['name', 'image', 'img_path', 'brand_name', 'price', 'store', 'category', 'garment_details']
                let prod_details = ['specific_name', 'colors', 'material', 'is_discounted', 'discount', 'description', 'subcategory', 'neck_design', 'design_pattern', 'sizes_available']
                switch (element_id) {
                    case '':
                        break;
                }
            }
            break;
        case 'Home Appliances':
            break;
    }
}

function OpenNextStep(step) {
    debugger;
    //let stepid = step + '_step';
    let tabid = step + '_tab';
    let disabled_steps = document.getElementsByClassName('disabled step')
    disabled_steps[0].classList.add('active')
    disabled_steps[0].classList.remove('disabled')
        // disabled_steps[0].classList.add('active')
    let active_steps = document.getElementsByClassName('active step')
    active_steps[0].classList.add('disabled')
    active_steps[0].classList.remove('active')

    //active_steps[0].classList.add('disabled')
    // let link = tabName + 'Link'
    // document.getElementById(link).classList.add('active')
    var a = document.querySelector('.ui.tab.active')
    if (a !== null)
        document.querySelector('.ui.tab.active').classList.remove('active');

    document.querySelector(`[id=${CSS.escape(tabid)}]`).classList.add('active');
}

function ProceedStep2() {
    //UpdateForm1()
    if (!ValidateProductInfo()) {
        DisplayMessage('Required Fields Missing', 'Complete the form below to proceed', false)

    } else {
        OpenNextStep('product_details')
    }
}

function process(id) {
    debugger
    const file = document.querySelector(`#${id}`).files[0];
    if (file.type == "image/jpeg" || file.type == "image/jpg" || file.type == "image/png") {
        if (!file) return;
        const reader = new FileReader();
        reader.readAsDataURL(file);
        let list = ["small_thumbnail", "thumbnail", "large"]
        reader.onload = function(event) {
            const imgElement = document.createElement("img");
            imgElement.src = event.target.result;
            // document.querySelector("#input").src = event.target.result;
            imgElement.onload = function(e) {
                let errorMsg = ''
                    //document.querySelector('#resolution').innerHTML = e.target.width+'&times'+e.target.height; 
                if (e.target.width < 600) {

                    errorMsg = '<li>Image Width should not be less than 600 px</li>'
                }
                if (e.target.height < 900) {
                    errorMsg += '<li>Image Height should not be less than 900 px</li>'
                }
                if (errorMsg != '') {
                    document.querySelector(`#${id}_errorLabel`).classList.remove('hidden')
                    document.querySelector(`#${id}_errorLabel`).innerHTML = errorMsg
                    DisplayMessage('Invalid Image File', errorMsg, false)
                    document.querySelector(`#${id}`).value = null
                    return
                } else {
                    document.querySelector(`#${id}_errorLabel`).classList.add('hidden')
                    document.querySelector(`#${id}_errorLabel`).innerHTML = errorMsg
                    document.querySelector('.showMessage').style.display = 'none'
                }
                let MAX_HEIGHT
                let srcEncoded
                let given_height = e.target.height
                let given_width = e.target.width
                for (item in list) {
                    switch (list[item]) {
                        case "thumbnail":
                            MAX_HEIGHT = 300
                            srcEncoded = ResizeImage(e, MAX_HEIGHT, true)
                            document.querySelector(`#output_${id}`).src = srcEncoded;
                            document.getElementById('image_handler').value = id
                            break;
                        case "large":
                            MAX_HEIGHT = 500
                            srcEncoded = ResizeImage(e, MAX_HEIGHT)
                            document.querySelector('#modal_preview').src = srcEncoded;
                            break;
                    }
                }
                // document.querySelector("a.ui.image").classList.remove('hidden')
                //document.querySelector('#modal_preview').src = srcEncoded;
                $('.ui.modal').modal('show');
                document.querySelector('#preview_modal').classList.add('active');
            };
        };
    } else {
        DisplayMessage('Invalid Image File', 'Allowed types are JPG/JPEG Or PNG', false)
        return false
    }
}

function ResizeImage(event, MAX_HEIGHT, is_thumbnail = false) {

    const canvas = document.createElement("canvas");
    //const MAX_HEIGHT = 200;
    let given_width = event.target.width
    let given_height = event.target.height
    if (is_thumbnail) {
        canvas.width = 300
        canvas.height = 350
    } else {
        if (given_height > 350 || given_width > 300) {
            const scaleSize = MAX_HEIGHT / given_height;
            canvas.width = given_width * scaleSize;
            canvas.height = MAX_HEIGHT;
        } else {
            canvas.width = given_width
            canvas.height = given_height
        }
    }
    const ctx = canvas.getContext("2d");
    ctx.drawImage(event.target, 0, 0, canvas.width, canvas.height);
    const srcEncoded = ctx.canvas.toDataURL(event.target, "image/jpeg");
    return srcEncoded
        // you can send srcEncoded to the server
}

function DiscardImage() {
    debugger
    let tag_id = document.getElementById('image_handler').value
    document.getElementById(tag_id).value = null
    document.getElementById('output_' + tag_id).src = null
}

function ValidateImg() {
    debugger
    const file = document.querySelector("#product_image").files[0];

    if (!file) return;

    const reader = new FileReader();

    reader.readAsDataURL(file);
    reader.onload = function(event) {
        const imgElement = document.createElement("img");
        imgElement.src = event.target.result;
        imgElement.onload = function(e) {
            if (e.target.width < 1100 || e.target.width > 2500) {
                console.log('invalid')
            }
            if (e.target.height < 1100 || e.target.height > 2500) {
                console.log('Invalid')
            }
        };
    };
}

function ValidateProductInfo() {
    let requiredFields = ['product_name', 'select-prodtype', 'product_price', 'product_image_front', 'product_image_rear', 'product_image_side', 'origin_country']
    let count = 0
    for (let field in requiredFields) {
        let productInfo = document.getElementById(requiredFields[field]).value
        let errorLabel = requiredFields[field] + '_errorLabel'
        if (productInfo != null && productInfo !== "") {
            document.getElementById(errorLabel).classList.add('hidden')
            continue
        } else {
            document.getElementById(errorLabel).classList.remove('hidden')
            document.getElementById(errorLabel).innerHTML = 'This Field is Required'
            count++
        }
    }
    if (count == 0)
        return true
    else
        return false
}