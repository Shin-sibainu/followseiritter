let click_count = 0 

// csrf_tokenの取得に使う
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


document.addEventListener('DOMContentLoaded', () => {
  countBtn  = document.getElementById('count-btn')
  countDisplay = document.getElementById('count-display')
  countBtn.addEventListener('click', () => {
    var csrf_token = getCookie("csrftoken");
    //クリックしたらクリック回数をカウントする。
    click_count += 1    
    console.log('you are clicked!')
    //console.log(click_count)
    $.ajax({
       type: 'post',
       url: '/getDataPra/',
       data: {
        "click_count": click_count,
    },
       //リクエストを送る前にトークンの確認。なければ送信しない。
       beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    },
       success: function(data){
         console.log(data)
         click_count_num = data.click_count
         countDisplay.innerHTML = click_count_num
       }
    })
  })
})
