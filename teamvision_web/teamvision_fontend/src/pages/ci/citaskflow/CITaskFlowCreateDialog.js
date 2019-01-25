//ci taskflow form validate rule

let ciTaskFlowValidateRules={
  Project: [
    { type: 'integer', required: true, message: '请选择项目或者创建项目后再创建任务流！' }
  ],
  FlowName: [
    { type: 'string', required: true, min: 1, max: 50, message: '标题长度必须在1-50个字符之间！', trigger: 'blur' }
  ],
  Description: [
    { type: 'string', required: false, max: 50, message: '描述信息长度不超过200个字符！', trigger: 'blur' }
  ]
}

export {
  ciTaskFlowValidateRules
}
