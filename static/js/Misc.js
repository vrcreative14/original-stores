
function Login() {
   debugger
   let credInput = document.getElementById('logincredInput').value
   let pw = document.getElementById('logincredInputpw').value
   let jsonBody=''
    if(!validateMobileno(credInput)){
      if(!validateEmail(credInput))
         DisplayMessage('','Invalid Input.Please correct the entry and try again', false)
         else{
             jsonBody = JSON.stringify({
                "email":credInput,
                "pft":pw
            })
         }
    }
    else{
         jsonBody = JSON.stringify({
            "phone":credInput,
            "pft":pw
        })
    }   
    
    postJSON('http://127.0.0.1:8000/api/login/', jsonBody)

}

// function logout() {
//     tkl = window.getCookie('tkl')
//     jsonBody = JSON.stringify({
//         '' : 
//     })
// }


function validateMobileno(enteredMobile) {
    debugger;
   
    // if (enteredMobile == undefined || enteredMobile == '')
    //   showMessage('mobileno',true)
    var regex = /^\d{10}$/;
    if( regex.test(String(enteredMobile).toLowerCase())){
         //showMessage('mobileno', false)
         isFormValid=true;
         return true;
    }
    else{
         //showMessage('mobileno', true)
         isFormValid=false;
         return false
    }
}

function validateEmail(email) {    
    
    var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    console.log(regex.test(String(email).toLowerCase()));
    
    if(regex.test(String(email).toLowerCase()))
    {       
        return true
    }
    else
    {        
      
        isFormValid=false;        
        return false
    }
}

const postJSON = (url, jsonBody) => {

    fetch(url,{ 
        method : 'POST',
        headers: {
        'Accept': "application/json, text/plain, */*",
        'Content-Type': 'application/json',     
        'Accept-Encoding':'gzip,deflate,br',
        'X-CSRFToken':csrftoken,      
        },
        body: jsonBody
    }
  )
        .then(response => {
            if(!response.ok){
            console.log(response)
            response.text().then(text => {
                DisplayMessage('','Some Error Occurred. Please try again after some time.', false)
            })
            // if(response.status == 400 || response.statusText == 'Bad Request'){
            //     let msg = 'Email Id or Phone Number already exists'
            //     document.getElementById('msg-heading').innerText = msg;            
            //     document.getElementById('msg-heading').className = 'errormsg';
            //     document.getElementById('msg-heading').style.display = 'block';
            // }
            //throw Error(response.statusText)
            }
            else{
                 return response.json()
                // console.log(response)
                // let msg = 'You have been Registered Successfully'
                // OpenMobileVerification()
                //  document.getElementById('modalmsg').innerText = msg;            
                //  document.getElementById('sellermodal').style.display = 'block';
                //  document.getElementById('msg-heading').style.display = 'none';
                //  if(mobile_no == ''){
                //  document.getElementById('phoneVerification').display='none';
                //  document.getElementById('phoneVerification').display='none';
                //  }
            }       
        })
        .then(data => {
            console.log(data)
            ShowResult(data);
        })
        .catch(error => console.log(error))

}

const postJSONAuth = (url, jsonBody) => {
    let tkl = getCookie('tkl')
    fetch(url,{ 
        method : 'POST',
        headers: {
        'Accept': "application/json, text/plain, */*",
        'Content-Type': 'application/json',     
        'Accept-Encoding':'gzip,deflate,br',
        'X-CSRFToken':csrftoken,
        'Authorization' : 'token ' + tkl     
        },
        body: jsonBody
    }
  )
        .then(response => {
            if(!response.ok){
            console.log(response)
            response.text().then(text => {
                DisplayMessage('','Some Error Occurred. Please try again after some time.', false)
            })
            // if(response.status == 400 || response.statusText == 'Bad Request'){
            //     let msg = 'Email Id or Phone Number already exists'
            //     document.getElementById('msg-heading').innerText = msg;            
            //     document.getElementById('msg-heading').className = 'errormsg';
            //     document.getElementById('msg-heading').style.display = 'block';
            // }
            //throw Error(response.statusText)
            }
            else{
                 return response.json()
                // console.log(response)
                // let msg = 'You have been Registered Successfully'
                // OpenMobileVerification()
                //  document.getElementById('modalmsg').innerText = msg;            
                //  document.getElementById('sellermodal').style.display = 'block';
                //  document.getElementById('msg-heading').style.display = 'none';
                //  if(mobile_no == ''){
                //  document.getElementById('phoneVerification').display='none';
                //  document.getElementById('phoneVerification').display='none';
                //  }
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
    fetch(url,{ 
        method : 'patch',
        headers: {
        'Accept': "*/*",
        'Content-Type': 'application/json;multipart/form-data',     
        'Accept-Encoding':'gzip,deflate,br',
        'X-CSRFToken':csrftoken,
        'Authorization' : 'token ' + tkl     
        },
        body: jsonBody
    }
  )
        .then(response => {
            if(!response.ok){
            console.log(response)
            response.text().then(text => {
                DisplayMessage('','Some Error Occurred. Please try again after some time.', false)
            })
            // if(response.status == 400 || response.statusText == 'Bad Request'){
            //     let msg = 'Email Id or Phone Number already exists'
            //     document.getElementById('msg-heading').innerText = msg;            
            //     document.getElementById('msg-heading').className = 'errormsg';
            //     document.getElementById('msg-heading').style.display = 'block';
            // }
            //throw Error(response.statusText)
            }
            else{
                 return response.json()
                // console.log(response)
                // let msg = 'You have been Registered Successfully'
                // OpenMobileVerification()
                //  document.getElementById('modalmsg').innerText = msg;            
                //  document.getElementById('sellermodal').style.display = 'block';
                //  document.getElementById('msg-heading').style.display = 'none';
                //  if(mobile_no == ''){
                //  document.getElementById('phoneVerification').display='none';
                //  document.getElementById('phoneVerification').display='none';
                //  }
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
        switch(data.detail){
            case 'An SMS with an OTP(One Time Password) has been sent <br/> to your Mobile number':                
                OpenMobileVerification();
                DisplayMessage('',data.detail,data.status)
                document.querySelector('#mobileField').classList.add('hidden')
                //document.querySelector('#signupBtn').classList.add('hidden')
               // OpenSignupForm()
                break;

            case 'Either phone or otp was not received':
                DisplayMessage('Required Data missing',data.detail,data.status)
                break;
            
            case 'User registered successfully':
                //DisplayMessage('Required Data missing',data.detail,data.status)
                debugger
                var pft = document.getElementById('password').value  
                var mobile_no = document.getElementById('mobile_no').value
                setCookie('user_ph',mobile_no)
                debugger
                document.getElementById('otpVerificationDiv').style.display = 'none';    
                $('.ui.modal').modal('show');
               
                let jsonBody = JSON.stringify({
                    'phone': mobile_no,
                    'pft': pft,
                })
                postJSON('http://127.0.0.1:8000/api/login/', jsonBody)
                debugger
                setTimeout(() => { window.open('/','_self') }, 2000);
                break;

            case 'OTP matched':
               // document.getElementById('otpmatchedIcon').style.display = 'inline';

                DisplayMessage('','Excellent! OTP Matched',data.status)
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
                    "storeimage" : img,
                    "store": data.store
                }
                if(img == '' || img == undefined){
                    //DisplayMessage('','Store Successfully Created. Now you are ready to list your products online and reach your customers.', true)
                    OpenModalProceed('/SellerDashboard','Store Successfully Created. Now you are ready to list your products online and reach your customers.','Redirecting you to Dashboard')
                    break;
                }
                postImage('http://127.0.0.1:8000/api/store/create/',JSON.stringify(dict))              
                break;
            case 'Image uploaded succcesfully':
                DisplayMessage('','Store Successfully Created. Now you are ready to list your products online and reach your customers.', true)

            default: 
                if(data.token !== undefined)   
                ProceedLogin(data)
                DisplayMessage('',data.detail,data.status)

        }
}


const OpenModalProceed = (pageurl,text,message) => {
    $('.ui.modal').modal('show');
    document.querySelector('.ui.modal > div > span').innerText = `${text}`
    document.querySelector('.content > p').innerText = `${message}`
    setTimeout(() => {  window.open(`${pageurl}`,'_self') }, 3000);
}

const ProceedLogin = (data) => {
  debugger
  tkldet = data.token
  setCookie('tkl',tkldet, data.expiry)
  $('.ui.modal').modal('show');
  document.querySelector('.ui.modal > div > span').innerText = 'Logged in Successfully'
  document.querySelector('.content > p').innerText = 'Redirecting you to home page..'
  setTimeout(() => {  window.open('/','_self') }, 3000);
}

const DisplayMessage = (heading,detail, status) =>{
    switch(status.toString()){
     case 'true':
        document.querySelector('.showMessage').classList.remove('error') ;
        document.querySelector('.showMessage').classList.add('success') ;
        break;
    case 'false':
        document.querySelector('.showMessage').classList.remove('success') ;
        document.querySelector('.showMessage').classList.add('error') ;
    case 'info':
    document.querySelector('.showMessage').classList.remove('success') ;
    document.querySelector('.showMessage').classList.remove('error') ;
    document.querySelector('.showMessage').classList.add('info') ;

    }
   
    document.querySelector('.showMessage').style.display='block'
    document.querySelector('.showMessage>div').innerText = heading
    document.querySelector('.showMessage>p').innerHTML = detail     
}

function setCookie(cname, cvalue, expires){
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
    for(var i = 0; i < ca.length; i++) {
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

