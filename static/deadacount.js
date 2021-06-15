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
//クエリ取得関数
function getParam(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}
//-------------------------------------------------------------


let clickcount_for_next_list = 0 
let isOverList = false

//クリックした時の動作。クリック数を取得。
document.addEventListener('DOMContentLoaded', function(){
  const loadBtnDead = document.getElementById('load-btn-dead')
  const loadBtnAlive = document.getElementById('load-btn-alive')
  loadBtnDead.addEventListener('click', function(){
    //Ajax通信を行う。
    console.log('you are clicked')
    clickcount_for_next_list += 1
    console.log(clickcount_for_next_list)
    handleGetApiData()
  })
  loadBtnAlive.addEventListener('click', function(){
    //Ajax通信を行う。
    console.log('you are clicked')
    clickcount_for_next_list += 1
    console.log(clickcount_for_next_list)
    handleGetApiData()
  })
})

//AjaxでTwitterAPIから持ってきたデータを受け取る関数。
const handleGetApiData = () => {
    var csrf_token = getCookie("csrftoken");
    const new_post_dead = document.getElementById('new_post_dead')
    const new_post_alive = document.getElementById('new_post_alive')
    const loadBtnDead = document.getElementById('load-btn-dead')
    const loadBtnAlive = document.getElementById('load-btn-alive')
    $.ajax({
      url: "/twitter_api_data/",
      type: 'POST',
      data: {
        'clickcount_for_next_list': clickcount_for_next_list,
        'screen_name_data': getParam('screen_name')
      },
       //リクエストを送る前にトークンの確認。なければ送信しない。
       beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    },
    success:function(response){
      console.log(response)
      const api_data_dead = response.deadacount_list
      const api_data_alive = response.aliveacount_list
      const isOverList = response.isOverList
      if(isOverList){
        new_post_dead.innerHTML += `<h4>以上です</h4>`
        new_post_alive.innerHTML += `<h4>以上です</h4>`
        loadBtnDead.remove()
        loadBtnAlive.remove()
      }
      else {
        api_data_dead.map(post => {
          new_post_dead.innerHTML += `<div id=twitter_info_box_dead>
                       <img src="${post.profile_image_url_https}" id="twitter_img">
                       <div class="user_info">
                       <p id="username">${post.name}</p>
                       <a href="${post.profile_url}" target="_blank" rel="noopener noreferrer">@${post.screen_name}</a>
                       </div>
                       </div>`
          })
        api_data_alive.map(post => {
          new_post_alive.innerHTML += `<div id=twitter_info_box_alive>
                       <img src="${post.profile_image_url_https}" id="twitter_img">
                       <div class="user_info">
                       <p id="username">${post.name}</p>
                       <a href="${post.profile_url}" target="_blank" rel="noopener noreferrer">@${post.screen_name}</a>
                       </div>
                       </div>`
        })
      }
    },
    error:function(error){
      console.log(error)
    }
  })
}
