import axios from 'axios'

let axiosSync = (url,data,method = 'post') => {
  let promise = new Promise(function (resolve, reject) {
    axios({
      method: method,
      url: url,
      data: data,
    }).then(function (res) {
      resolve(res)
    }).catch(function (err) {
      // reject(err)
    })
  })
  return promise
}

export {
  axiosSync
}
