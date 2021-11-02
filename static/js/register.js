
document.getElementById("register-but").addEventListener("click",()=>{
    password1 = document.getElementById("password1").value;
    password2 = document.getElementById("password2").value;
    username = document.getElementById("uname").value;
    email = document.getElementById("email").value;
    if (password1 != password2){
        alert("please enter the same password!");
    }else {
        fetch('/register/',{
            method:"POST",
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'username':username,
            'password':password1,
            'email':email,
        })
        }.then((response)=>{
            if(response.status == 400){
                response.text().then((data) => {
                console.log(data);
            });
            } else if (response.status == 200) {
                response.json().then((data)=>{
                    console.log(data);
                })
            }else if (response.status == 200) {
                 response.text().then((data) => {
                console.log(data);})
            }
            }).catch((err) => {
            console.log('Error in registion: ', err);})

        )
    }



});


