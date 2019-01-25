//ci taks validate rule

let responseValidateRules={
  Description: [
    { type: 'string', required: true, message: '响应描述为必填项', trigger: 'blur' }
  ],
  Response: [
    { type: 'string', required: true, message: '响应值为必填项！', trigger: 'blur' }
  ]
}

export {
  responseValidateRules
}
