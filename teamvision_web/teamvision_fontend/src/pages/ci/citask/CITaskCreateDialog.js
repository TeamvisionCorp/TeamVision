//ci taks validate rule

let ciTaskValidateRules={
  Project: [
    { type: 'integer', required: true, message: '请选择项目或者创建项目后再创建任务！' }
  ],
  TaskName: [
    { type: 'string', required: true, min: 1, max: 50, message: '标题长度必须在1-50个字符之间！', trigger: 'blur' }
  ],
  TaskType: [
    { type: 'integer', required: true,message: '任务类型是必选项' }
  ],
  CopyTaskID: [
    { type: 'integer',message: '请选择要复制的任务' }
  ]
}

export {
  ciTaskValidateRules
}
