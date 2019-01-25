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

let initTaskForm = (taskID) => {
    let defaultTask={
        id: taskID,
        Title: '',
        Owner: 0,
        Priority: '3',
        DeadLine: '',
        WorkHours: 8,
        Description: '',
        ProjectID: [],
        childTask: {
          index: 1,
          items: [
            {
              value: '',
              index: 1,
              status: 1,
              active: 1
            }
          ]
        },
      }
    let initPromise = new Promise(function (resolve, reject) {
      axios.get('/api/project/task/' + taskID).then(response => {
        let initData=response.data.result
        resolve(initData)
      }, response => {
        resolve(defaultTask)
      })
    })
  return initPromise
}

let taskValidateRules={
  ProjectID: [
    { type: 'array', required: true,len: 2, message: '请选择版本或者创建版本后再创建任务！' }
  ],
  Title: [
    { type: 'string', required: true, min: 1, max: 50, message: '标题长度必须在1-50个字符之间！', trigger: 'blur' }
  ],
  WorkHours: [
    { type: 'integer', required: true, message: '请输入工时！' }
  ]
}

export {
  initProjectVersions,
  taskValidateRules,
  initTaskForm
}
