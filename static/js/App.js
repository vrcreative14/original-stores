function getCoordinates() {
    debugger
    var locat = document.getElementById("storelocation")
    if (navigator.geolocation) {
        location = navigator.geolocation.getCurrentPosition();

    } else {
        document.getElementsByClassName('showMessage').innerHTML = "Geolocation is not supported by this browser.";
    }
}

function getLocation() {
    var locat = document.getElementById("storelocation")
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        document.getElementsByClassName('showMessage').innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    debugger;
    //getLocation();
    var loc = document.getElementById('save')
    fetchLocationName(position);
    //l.placeholder = "Latitude: " + position.coords.latitude +
    //"<br>Longitude: " + position.coords.longitude;
    document.getElementById('latitude').value = position.coords["latitude"]
    document.getElementById('longitude').value = position.coords["longitude"]
}

function fetchLocationName(position) {
    const proxyurl = "https://cors-anywhere.herokuapp.com/";
    const url = `http://apis.mapmyindia.com/advancedmaps/v1/99gsfvaspt7kg4nz13g3hg1bvsvkx48j/rev_geocode?lat=${position.coords.latitude}&lng=${position.coords.longitude}`;
    fetch(proxyurl + url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
                'csrfmiddlewaretoken': csrftoken,
            },
        })
        .then(response => response.json())
        .then(function(data) {
            console.log(data)
            document.getElementById('saveLocation').value = JSON.stringify(data.results[0])
            let currentEvent = document.getElementById('currentEvent').value
                // FillAddress(data.results[0])
            switch (currentEvent) {
                case 'detectLocation':
                    FillCitynPin(data.results[0])
                    break;
                case 'detect-location':
                    FillAddress(data.results[0])
                    break;
                default:
                    break;
            }

        })
}

function DetectLocation(data) {
    var locationInput = document.querySelector('#locationInput')
    if (locationInput != null) {
        locationInput.value = data["pincode"]
    }

}

function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}
//fetchStores();
//getLocation();
function fetchStores() {
    var wrapper = document.getElementById('storeListDiv')
        //wrapper.innerHTML=''
    console.log('fetching....')
    fetch('http://www.vcnity.online/api/store-list/', {
            method: 'GET',
        })
        .then(response => response.json())
        .then(function(data) {
            console.log(data)
            var list = data
            for (let i in list) {
                var title = `<span class="title">${list[i].shopName}</span>`
                console.log(title)
                console.log(list[i].imgPath)
                try {
                    var desc = `
           <div>
                   <div style="background-image: url(${list[i].imgPath});" class="productDesc" alt="hello">                   
                   </div>
                   <a href="#"> ${title}</a>
                   </div>
           `
                    wrapper.innerHTML += desc
                } catch {
                    continue;
                }
            }
        })
}

//showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

//Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

// function showSlides(n) {
// var i;
// var slides = document.getElementsByClassName("mySlides");
// var dots = document.getElementsByClassName("dot");  
// if (n > slides.length) {slideIndex = 1}
// if (n < 1) {slideIndex = slides.length}
// for (i = 0; i < slides.length; i++) {
//    slides[i].style.display = "none";
// }
// for (i = 0; i < dots.length; i++) {
//    dots[i].className = dots[i].className.replace(" active", "");
// }
// slides[slideIndex-1].style.display = "block";
// dots[slideIndex-1].className += " active";  
// }

var docWidth = document.documentElement.offsetWidth;

[].forEach.call(
    document.querySelector('*'),
    function(e1) {
        if (e1.offsetWidth > docWidth) {
            console.log(e1);
        }
    }
);

function autoSlide(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > slides.length) { slideIndex = 1 }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace("active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
    setTimeout(showSlides, 2000); //change image every 2 seconds
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            //Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function openTab(tabName) {
    debugger;
    var activeLink = document.getElementsByClassName('item step active')
    activeLink[0].classList.add('disabled')
    activeLink[0].classList.remove('active')
    let link = tabName + 'Link'
    document.getElementById(link).classList.add('active')
    var a = document.querySelector('.ui.tab.active')
    if (a !== null)
        document.querySelector('.ui.tab.active').classList.remove('active');

    document.querySelector(`[name=${CSS.escape(tabName)}]`).classList.add('active');
    document.querySelector(`[id=${CSS.escape(link)}]`).classList.remove('disabled');
    window.scroll({
        top: 100,
        left: 0,
        behavior: 'smooth'
    });
}




// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function setCookie(cname, cvalue, expires) {
    var d = new Date();
    var t = new Date(Date.parse(expires));
    // d.setTime(parseInt(d.getTime() + (t.getTime() * 24*60*60*1000)));
    var expires = "expires=" + t.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

window.onload = function() {

    let msg = getCookie('messageText')
    let status = getCookie('messageType')
    if (msg != "") {
        DisplayMessage('', msg, status)
        setCookie('messageText', '')
    }
    //document.getElementById('messageText').value = ""

    // if (tkl == undefined || tkl == ''){
    //     var headerLinks=document.querySelectorAll('.navbar > .signedout')
    //     for(let i=0;i<headerLinks.length;i++){
    //         headerLinks[i].classList.remove('hidden')
    //     }
    // }

    // else {
    // var headerLinks=document.querySelectorAll('.navbar > .signedin')
    // for(let i=0;i<headerLinks.length;i++){
    //     headerLinks[i].classList.remove('hidden')
    // }
    //}

    //FetchCitynPin()
}



function getCookie(cname) {
    debugger
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function FetchCitynPin(event) {
    document.getElementById('detectLocation').classList.add('loading')
    if (!!event)
        document.getElementById('currentEvent').value = event.target.id

    debugger
    let location = ""
    getLocation()
        // location = JSON.parse(document.getElementById('saveLocation').value)
        // if(location != "" && location !== undefined) {       
        //     FillCitynPin(location)    
        // }   

    // else
    // DisplayMessage('', 'Not able to detect location at this time' ,false)

}

function FillCitynPin(data) {
    if (data == undefined || data == "") {

    }
    let pin = data["pincode"]
    let city = data["city"]
    let area = data["subLocality"]
    document.getElementById('locationCity').value = city + " , " + area
    document.getElementById('locationPin').value = pin
    document.getElementById('detectLocation').classList.remove('loading')
}

function ShowMessageBar() {
    var x = document.getElementById("messagebar");
    x.className = "show";
    setTimeout(function() { x.className = x.className.replace("show", ""); }, 3000);
}

function GoToPage(url, val) {
    window.open(url, "_self")
}