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

let initFortestingForm = (fortestingID) => {
    let defaultTask={
        id: fortestingID,
      Topic: '',
      ProjectModuleID: 0,
      CodeRepertory: '',
      Branch: '',
      TestingAdvice: '',
      TestingFeature: '',
      ProjectVersion: [],
      attachments: {
        defaultList: [

        ],
        imgName: '',
        visible: false,
        uploadList: []
      }
      }
    let initPromise = new Promise(function (resolve, reject) {
      axios.get('/api/project/fortesting/' + fortestingID).then(response => {
        let initData=response.data.result
        resolve(initData)
      }, response => {
        resolve(defaultTask)
      })
    })
  return initPromise
}

let fortestingValidateRules={
  ProjectVersion: [
    { type: 'array', required: true,len: 2, message: '请选择版本或者创建版本后再创建提测！' }
  ],
  ProjectModuleID: [
    { type: 'integer', required: true, message: '请选择模块！' }
  ],
  Topic: [
    { type: 'string', required: true, min: 1, max: 50, message: '标题长度必须在1-50个字符之间！', trigger: 'blur' }
  ],
  TestingFeature: [
    { type: 'string', required: true, message: '提测内容为必选内容' }
  ],
  TestingAdvice: [
    { type: 'string', required: true, message: '请填写提测建议' }
  ]
}

export {
  initProjectVersions,
  fortestingValidateRules,
  initFortestingForm
}
