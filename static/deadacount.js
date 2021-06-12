//let isclicked = false

//AjaxでTwitterAPIから持ってきたデータを受け取る関数。
const handleGetApiData = () => {
    const new_post = document.getElementById('new_post')
    console.log('handle loaded')
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
}

document.addEventListener('DOMContentLoaded', function(){
  const loadBtn = document.getElementById('load-btn')
  loadBtn.addEventListener('click', function(){
    //Ajax通信を行う。
    console.log('you are clicked')
    handleGetApiData()
  })
})
