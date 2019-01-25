
//初始化webapp body height
function initWebapp () {
  var windowHeight=window.innerHeight
  var appBody=document.getElementById('appBody')
  appBody.style.height=(windowHeight-120)+'px'
  console.log(document.cookie.length)
}

export {
  initWebapp
}
