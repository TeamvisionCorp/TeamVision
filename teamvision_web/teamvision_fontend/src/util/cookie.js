const getCookie = function (name) {
  var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)")
  if (arr = document.cookie.match(reg))
    return (arr[2]);
  else
    return null;
}

export {
  getCookie
}
