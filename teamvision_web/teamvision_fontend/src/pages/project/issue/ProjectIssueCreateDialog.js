//初始化项目以及版本信息
import axios from 'axios'
let initProjectVersions = function (tempData) {
  let projectVersions=[]
  for (let i=0;i<tempData.length;i++)
  {
    let tempProject={}
    tempProject.value=tempData[i].id
    tempProject.label=tempData[i].PBTitle
    tempProject.children=[]
    for (let j=0;j<tempData[i].Versions.length;j++)
    {
      let tempChild={}
      tempChild.label=tempData[i].Versions[j].VVersion
      tempChild.value=tempData[i].Versions[j].id
      tempProject.children.push(tempChild)
    }
    projectVersions.push(tempProject)
  }
  return projectVersions
}


let issueValidateRules={
  Project: [
    { type: 'array', required: true,len: 2, message: '请选择版本或者创建版本后再创建任务！' }
  ],
  Title: [
    { type: 'string', required: true, min: 1, max: 100, message: '问题标题长度在1-100个字符之间', trigger: 'blur' }
  ],
  Processor: [
    { type: 'number', required: true, min: 1, message: '请指派问题处理人' }
  ],
  Team: [
    { type: 'number', required: true, min: 1, message: '请选择问题所属角色' }
  ],
  Module: [
    { type: 'number', required: true, min: 1, message: '请选择问题业务模块' }
  ],
  Severity: [
    { type: 'number', required: true, min: 1, message: '请选择问题严重性' }
  ],
  IssueCategory: [
    { type: 'number', required: true, min: 1, message: '请选择问题类别' }
  ],
  ProjectPhase: [
    { type: 'number', required: true, min: 1, message: '请选择问题发现阶段' }
  ],
  Priority: [
    { type: 'number', required: true, min: 1, message: '请选择问题优先级' }
  ]
}

export {
  initProjectVersions,
  issueValidateRules,
}
