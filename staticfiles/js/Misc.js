const csrftoken = getCookie('csrftoken');
const tkl = ""

function Login() {
    debugger
    let credInput = document.getElementById('logincredInput').value
    let pw = document.getElementById('logincredInputpw').value
    let jsonBody = ''
    if (!validateMobileno(credInput)) {
        if (!validateEmail(credInput))
            DisplayMessage('', 'Invalid Input.Please correct the entry and try again', false)
        else {
            jsonBody = JSON.stringify({
                "email": credInput,
                "pft": pw
            })
        }
    } else {
        jsonBody = JSON.stringify({
            "phone": credInput,
            "pft": pw
        })
    }
    postJSON('/api/login/', jsonBody)
}

function Logout() {
    debugger
    let jsonBody = ''
    getID(postLogout, '/api/logout/', jsonBody)
}

function validateMobileno(enteredMobile) {
    debugger;

    // if (enteredMobile == undefined || enteredMobile == '')
    //   showMessage('mobileno',true)
    var regex = /^\d{10}$/;
    if (regex.test(String(enteredMobile).toLowerCase())) {
        //showMessage('mobileno', false)
        isFormValid = true;
        return true;
    } else {
        //showMessage('mobileno', true)
        isFormValid = false;
        return false
    }
}

function validateEmail(email) {

    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    console.log(regex.test(String(email).toLowerCase()));

    if (regex.test(String(email).toLowerCase())) {
        return true
    } else {

        isFormValid = false;
        return false
    }
}

const postJSON = (url, jsonBody) => {

    fetch(url, {
            method: 'POST',
            headers: {
                'Accept': "application/json, text/plain, */*",
                'Content-Type': 'application/json',
                'Accept-Encoding': 'gzip,deflate,br',
                'X-CSRFToken': csrftoken,
            },
            body: jsonBody
        })
        .then(response => {
            if (!response.ok) {
                console.log(response)
                response.text().then(text => {
                    let detail = JSON.parse(text).detail;
                    DisplayMessage('', detail, false)
                })
            } else {
                return response.json()
            }
        })
        .then(data => {
            console.log(data)
            ShowResult(data);
        })
        .catch(error => console.log(error))

}

function postJSONAuth(url, jsonBody, tkl) {
    debugger
    if (tkl == "")
        DisplayMessage('You have been logged out', 'Log in Again to continue', 'info')
    fetch(url, {
            method: 'POST',
            headers: {
                'Accept': "application/json, text/plain, */*",
                'Content-Type': 'application/json',
                'Accept-Encoding': 'gzip,deflate,br',
                'X-CSRFToken': csrftoken,
                'Authorization': 'token ' + tkl
            },
            body: jsonBody,
        })
        .then(response => {
            if (!response.ok) {
                console.log(response)
                if (response.status == 401) {
                    DisplayMessage('You have been Logged Out', 'Log in again to continue..', false)
                    window.open("/login", "_self")
                }
                response.text().then(text => {
                    DisplayMessage('', 'Some Error Occurred. Please try again after some time.', false)
                })

            } else {
                return response.json()
            }
        })
        .then(data => {
            console.log(data)
            debugger
            ShowResult(data);
        })
        .catch(error => console.log(error))
}

const postImage = (url, jsonBody) => {
    let tkl = getCookie('tkl')
    fetch(url, {
            method: 'patch',
            headers: {
                'Accept': "*/*",
                'Content-Type': 'application/json;multipart/form-data',
                'Accept-Encoding': 'gzip,deflate,br',
                'X-CSRFToken': csrftoken,
                'Authorization': 'token ' + tkl
            },
            body: jsonBody
        })
        .then(response => {
            if (!response.ok) {
                console.log(response)
                response.text().then(text => {
                    DisplayMessage('', 'Some Error Occurred. Please try again after some time.', false)
                })
            } else {
                return response.json()
            }
        })
        .then(data => {
            console.log(data)
            debugger
            ShowResult(data);
        })
        .catch(error => console.log(error))

}

const ShowResult = (data) => {
    var detail = data.detail
    var status = data.status
    if (status == false) {
        switch (data.detail) {
            case 'Either phone or otp was not received':
                DisplayMessage('Required Data missing', data.detail, data.status)
                break;

            default:
                DisplayMessage('Some Error Occured.Please try again later', data.detail, data.status)
                break;

        }
    } else {
        switch (data.detail) {
            case 'An SMS with an OTP(One Time Password) has been sent <br/> to your Mobile number':
                OpenMobileVerification();
                DisplayMessage('', data.detail, data.status)
                document.querySelector('#mobileField').classList.add('hidden')
                break;
            case 'User registered successfully':
                debugger
                var pft = document.getElementById('password').value
                var mobile_no = document.getElementById('mobile_no').value
                debugger
                document.getElementById('otpVerificationDiv').style.display = 'none';
                $('.ui.modal').modal('show');

                let jsonBody = JSON.stringify({
                    'phone': mobile_no,
                    'pft': pft,
                })
                postJSON('/api/login/', jsonBody)
                debugger
                setTimeout(() => { window.open('/', '_self') }, 2000);
                break;

            case 'OTP matched':

                DisplayMessage('', 'Excellent! OTP Matched', data.status)
                OpenSignupForm()
                document.querySelector('#signupBtn').classList.remove('hidden')
                document.querySelector('#changemobileBtn').classList.remove('hidden')
                document.querySelector('#otpVerificationDiv').classList.add('hidden')
                document.querySelector('#otpVerificationDiv').classList.add('hidden')
                document.querySelector('#invalidPhoneLabel').classList.remove('red')
                document.querySelector('#invalidPhoneLabel').classList.add('green')
                document.querySelector('#invalidPhoneLabel').style.display = 'inline'
                document.querySelector('#invalidPhoneLabel').innerText = 'Verified through OTP'
                window.scrollBy(0, -300);

                break;
            case 'Logged in Successfully':
                ProceedLogin(data)

                break;

            case 'Store Successfully Created. Continue saving further information':
                debugger
                //openTab('taxInfo')
                //document.getElementsByClassName('showMessage').style.display = 'block'
                let img = document.getElementById('storeimage').value
                var dict = {
                    "storeimage": img,
                    "store": data.store
                }
                if (img == '' || img == undefined) {
                    //DisplayMessage('','Store Successfully Created. Now you are ready to list your products online and reach your customers.', true)
                    OpenModalProceed('/SellerDashboard', 'Store Successfully Created. Now you are ready to list your products online and reach your customers.', 'Redirecting you to Dashboard')
                    break;
                }
                postImage('http://www.vcnity.online/api/store/create/', JSON.stringify(dict))
                break;
            case 'Image uploaded succcesfully':
                DisplayMessage('', 'Store Successfully Created. Now you are ready to list your products online and reach your customers.', true)
            case 'You have been logged out Successfully.':
                DisplayMessage('', data.detail, data.status)
                setTimeout(() => { window.open("/", "_self") }, 2000);
                break;
            case 'Seller registered successfully. Continue filling the Store Info':
                openTab('storeInfo')
                DisplayMessage('', data.detail, data.status)
                break;
            case 'Product added succesfully':
                debugger
                OpenNextStep('product_details')
                DisplayMessage('Product Added Successfully in your Online Store', 'Continue adding product details to complete the process', true)
                document.getElementById('product_specific_name').value = document.getElementById('product_name').value + document.getElementById('brand_name').value
                document.getElementById('product_id').value = data.data
                document.getElementById('product_id').innerText = data.data
                break;
            case 'Shipping Address Saved Successfully':

                break;
            default:
                if (data.token !== undefined)
                    ProceedLogin(data)
                DisplayMessage('', data.detail, data.status)
        }
    }
}

const postLogout = (url, jsonBody, tkl) => {
    fetch(url, {
            method: 'POST',
            headers: {
                'Accept': "application/json, text/plain, */*",
                'Content-Type': 'application/json',
                'Accept-Encoding': 'gzip,deflate,br',
                'X-CSRFToken': csrftoken,
                'Authorization': 'token ' + tkl
            },
        })
        .then(response => {
            if (!response.ok) {
                console.log(response)
                if (response.status == 200) {
                    window.open("/", "_self")
                    DisplayMessage('You have been Logged Out', 'Log in again to continue..', false)
                }
                response.text().then(text => {
                    DisplayMessage('', 'Some Error Occurred. Please try again after some time.', false)
                })

            } else {
                return response.json()
                DisplayMessage('Error Occured', 'Please try again after some time', false)
            }
        }).then(data => {
            console.log(data)
            debugger
            ShowResult(data);
        }).catch(error => console.log(error))
}

const OpenModalProceed = (pageurl, text, message) => {
    $('.ui.modal').modal('show');
    document.querySelector('.ui.modal > div > span').innerText = `${text}`
    document.querySelector('.content > p').innerText = `${message}`
    setTimeout(() => { window.open(`${pageurl}`, '_self') }, 3000);
}

const ProceedLogin = (data) => {
    debugger
    tkldet = data.token
        // setCookie('tkl',tkldet, data.expiry)
    $('.ui.modal').modal('show');
    document.querySelector('.ui.modal > div > span').innerText = 'Logged in Successfully'
    document.querySelector('.content > p').innerText = 'Redirecting you to home page..'
    setTimeout(() => { window.open('/', '_self') }, 3000);
}

const DisplayMessage = (heading, detail, status) => {
    debugger
    switch (status.toString()) {
        case 'true':
            document.querySelector('.showMessage').classList.remove('error');
            document.querySelector('.showMessage').classList.add('success');
            break;
        case 'false':
            document.querySelector('.showMessage').classList.remove('success');
            document.querySelector('.showMessage').classList.add('error');
            break;
        case 'info':
            document.querySelector('.showMessage').classList.remove('success');
            document.querySelector('.showMessage').classList.remove('error');
            document.querySelector('.showMessage').classList.add('info');
            break;
    }

    document.querySelector('.showMessage').style.display = 'block'
    document.querySelector('.showMessage>div').innerText = heading
    document.querySelector('.showMessage>p').innerHTML = typeof(detail) == "object" ? (detail.length == 0 ? "" : detail[0]) : detail
}

function setCookie(cname, cvalue, expires) {
    var d = new Date();
    var t = new Date(Date.parse(expires));
    // d.setTime(parseInt(d.getTime() + (t.getTime() * 24*60*60*1000)));
    var expires = "expires=" + t.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
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

function checkCookie() {
    var username = getCookie("username");
    if (username != "") {
        alert("Welcome again " + username);
    } else {
        username = prompt("Please enter your name:", "");
        if (username != "" && username != null) {
            setCookie("username", username, 365);
        }
    }
}

function getID(callback, url, jsonBody) {
    idurl = '/api/get/id/'
    fetch(idurl, {
            method: 'GET',
            headers: {
                'Accept': "application/json, text/plain, */*",
                'Content-Type': 'application/json',
                'Accept-Encoding': 'gzip,deflate,br',
                'X-CSRFToken': csrftoken,
            },
            credentials: 'include',
        })
        .then(response => {
            debugger
            if (!response.ok) {
                console.log(response)
                response.text().then(text => {
                    let detail = JSON.parse(text).detail[0];
                    DisplayMessage('', detail, false)
                })
            } else {
                return response.json()
            }
        })
        .then(data => {
            debugger
            console.log(data)
            callback(url, jsonBody, data.tkl);
        })
        .catch(error => console.log(error))

}

function AddProduct(url, formData, tkl) {
    var headers = new Headers();
    headers.append("Cookie", `csrftoken =${csrftoken}`);

    // var formdata = new FormData();
    // formdata.append("product_name", "Sweater");
    // formdata.append("image", fileInput.files[0], "/D:/Images/Shop/1410028_outerknown_Fisherman_sweater_HEA_f_pdp_c_1400x1400.jpg");
    // formdata.append("brand_name", ".Raymonds\n\n499\n\n\n \"Duke\"");
    // formdata.append("product_price", "899");
    let requestOptions = ''

    if (url == 'api/product/add/') {
        requestOptions = {
            method: 'POST',
            headers: headers,
            body: formData,
            redirect: 'follow'
        };
    } else {
        requestOptions = {
            method: 'PUT',
            headers: headers,
            body: formData,
            redirect: 'follow'
        };
    }


    fetch(url, requestOptions)
        .then(
            response => response.text()
        )
        .then(result => {
            ShowResult(JSON.parse(result));
        })
        .catch(error => console.log('error', error));
}


function OpenMessageBar(text) {
    var bar = document.getElementById("messagebar");
    bar.className = "show";
    bar.innerText = text
    setTimeout(function() { bar.className = bar.className.replace("show", ""); }, 6000);
}