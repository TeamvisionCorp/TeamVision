//project validate rule

let projectValidateRules={
  PBTitle: [
    { type: 'string',min: 1, max: 50, required: true, message: '标题长度必须在1-50个字符！！' }
  ],
  PBKey: [
    { type: 'string', required: true, min: 1, max: 10, pattern: /^[A-Z]+$/, message: 'Key必须是10个以内的大写英文字符！', trigger: 'blur' }
  ],
  PBPlatform: [
    { type: 'integer', required: true,message: '请选择项目平台' }
  ],
  PBLead: [
    { type: 'integer', required: true,message: '请选择项目负责人' }
  ],
  Product: [
    { type: 'integer',required: true,message: '请选择产品线' }
  ]
}

export {
  projectValidateRules
}
