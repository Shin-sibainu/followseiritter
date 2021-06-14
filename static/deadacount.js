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


//-------------------------------------------------------------
let clickcount_for_next_list = 0 

//クリックした時の動作。クリック数を取得。
document.addEventListener('DOMContentLoaded', function(){
  const loadBtn = document.getElementById('load-btn')
  loadBtn.addEventListener('click', function(){
    //Ajax通信を行う。
    console.log('you are clicked')
    clickcount_for_next_list += 1
    console.log(clickcount_for_next_list)
    handleGetApiData()
  })
})

//クリックカウントをPythonへ渡すためのAjaｘ
/*
const getClickCount = () => {
  $.ajax({
    url: "/getDataPra/",
    type: 'POST',
    data: {
      'clickcount_for_next_list': clickcount_for_next_list
    },
    success: function(data){
      click_count_num = data.clickcount_for_next_list
      console.log(click_count_num)
    },
    error: function(error){
      console.log(error)
    }
  })
}
*/

//AjaxでTwitterAPIから持ってきたデータを受け取る関数。
const handleGetApiData = () => {
    var csrf_token = getCookie("csrftoken");
    const new_post = document.getElementById('new_post')
    $.ajax({
      url: "/twitter_api_data/",
      type: 'POST',
      data: {
        'clickcount_for_next_list': clickcount_for_next_list
      },
       //リクエストを送る前にトークンの確認。なければ送信しない。
       beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    },
    success:function(response){
      console.log(response)
      //const click_count = response.clickcount_for_next_list
      //console.log(click_count)
      const api_data = response.deadacount_list
      api_data.map(post => {
        new_post.innerHTML += `<div id=twitter_info_box>
                     <img src="${post.profile_image_url_https}" id="twitter_img">
                     <div class="user_info">
                     <p id="username">${post.name}</p>
                     <a href="${post.profile_url}" target="_blank" rel="noopener noreferrer">@${post.screen_name}</a>
                     </div>
                     </div>`
      })
    },
    error:function(error){
      console.log(error)
    }
  })
    /*
    $.ajax({
      type:'GET',
      url:'/twitter_api_data/',
      success:function(response){
        console.log(response)
        const api_data = response.deadacount_list
        api_data.map(post => {
          new_post.innerHTML += `<div id=twitter_info_box>
                       <img src="${post.profile_image_url_https}" id="twitter_img">
                       <div class="user_info">
                       <p id="username">${post.name}</p>
                       <a href="${post.profile_url}" target="_blank" rel="noopener noreferrer">@${post.screen_name}</a>
                       </div>
                       </div>`
        })
      },
      error:function(error){
        console.log(error)
      }
    })
    */
}
