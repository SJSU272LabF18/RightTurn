function onSuccess(googleUser) {
     document.getElementById('name').innerText =googleUser.getBasicProfile().getName();
     document.getElementById('email').innerText =googleUser.getBasicProfile().getEmail();
     document.getElementById('pic').src = googleUser.getBasicProfile().getImageUrl();
     }

function onFailure(error) {
      console.log(error);
    }