<template>
  <Modal :value="dialogShow" title="添加新任务" :width="600" @on-cancel="cancel" :styles="{bottom:'20px',top: '50px'}">
    <div :style="'height:' + containerHeight + 'px;overflow-y: scroll;overflow-x: hidden'">
      <Form ref="createTask" :model="formItem" :label-width="80" :rules="ruleCustom">
        <FormItem label="版本" prop="project">
          <Cascader v-model="formItem.ProjectID" :data="projectVersions" @on-change="onProjectChange"
                    :filterable="true"></Cascader>
        </FormItem>
        <FormItem label="标题" prop="Title">
          <Input v-model="formItem.Title" placeholder="任务标题"/>
        </FormItem>
        <FormItem label="执行者">
          <Select v-model="formItem.Owner" :filterable="true" placeholder="默认为创建者">
            <Option v-for="member in projectMembers" :key="member.PMMember" :value="member.PMMember">{{ member.name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="截止时间">
          <DatePicker type="date" placeholder="默认T+1完成" v-model="formItem.DeadLine"></DatePicker>
        </FormItem>
        <FormItem label="工时" prop="WorkHours">

          <Input v-model="formItem.WorkHours" :number="true" placeholder="默认8小时"/>

        </FormItem>
        <FormItem label="优先级">
          <RadioGroup v-model="formItem.Priority">
            <Radio label="3">普通</Radio>
            <Radio label="2">紧急</Radio>
            <Radio label="1">非常紧急</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="备注:">
          <Input v-model="formItem.Description" type="textarea" :autosize="{minRows: 2,maxRows: 5}"
                 placeholder="Enter something..."></Input>
        </FormItem>
        <div style="border-top: 1px solid rgba(0,0,0,.1);"></div>
        <div style="font-size: 14px;padding-top: 5px;color:#495060">
          <Icon type="navicon" :size="14"></Icon>
          子任务
        </div>
        <FormItem style="margin-left: -30px;" v-for="(item, index) in formItem.childTask.items" :key="index"
                  v-if="item.active" :prop="'childTask.items.' + index + '.value'"
                  :rules="{min:1,max:50,required: true, message: 'Item ' + index +' can not be empty',message:'任务内容长度1-30个字符！', trigger: 'blur'}">
          <Row>
            <Col span="2">
            <Checkbox v-model="item.status" :true-value="1" :false-value="0"></Checkbox>
            </Col>
            <Col span="18" style="text-align: center">
            <Input v-model="item.value" placeholder="输入任务内容"/></Col>
            <Col span="4">
            <span @click="handleRemove(index)"><Icon type="ios-trash" class="cursor-hand" :size="20"
                                                     style="margin-left: 30px; color:gray;"></Icon></span>
            </Col>
          </Row>
        </FormItem>
        <div>
          <span class="cursor-hand" @click="handleAdd"><Icon type="md-add-circle" :size="18"
                                                             color="#32be77"></Icon> <span>添加子任务</span></span>

        </div>
        <!--<div style="border-top: 1px solid rgba(0,0,0,.1);margin-top: 20px;"></div>-->
        <!--<div style="font-size: 14px;padding-top: 5px;color:#495060"><Icon type="android-attach" :size="14"></Icon> 附件</div>-->
        <!--<FormItem>-->
        <!--<div class="demo-upload-list" :key="index" v-for="(item,index) in formItem.attachments.uploadList">-->
        <!--<template v-if="item.status === 'finished'">-->
        <!--<img :src="item.url">-->
        <!--<div class="demo-upload-list-cover">-->
        <!--&lt;!&ndash;<Icon type="ios-eye-outline" @click.native="handleView(item.name)"></Icon>&ndash;&gt;-->
        <!--<Icon type="ios-trash-outline" @click.native="handleRemove2(item)"></Icon>-->
        <!--</div>-->
        <!--</template>-->
        <!--<template v-else>-->
        <!--<Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>-->
        <!--</template>-->
        <!--</div>-->
        <!--<Upload-->
        <!--ref="upload"-->
        <!--:show-upload-list="false"-->
        <!--:default-file-list="formItem.attachments.defaultList"-->
        <!--:on-success="handleSuccess"-->
        <!--:format="['jpg','jpeg','png']"-->
        <!--:max-size="2048"-->
        <!--:on-format-error="handleFormatError"-->
        <!--:on-exceeded-size="handleMaxSize"-->
        <!--:before-upload="handleBeforeUpload"-->
        <!--multiple-->
        <!--type="drag"-->
        <!--action="//jsonplaceholder.typicode.com/posts/"-->
        <!--style="display: inline-block;width:58px;">-->
        <!--<div style="width: 58px;height:58px;line-height: 58px;">-->
        <!--<Icon type="camera" size="20"></Icon>-->
        <!--</div>-->
        <!--</Upload>-->
        <!--</FormItem>-->
      </Form>
    </div>
    <div slot="footer">
      <Button v-if="createDialogShow" type="success" style="width: 80px; height:30px;" shape="circle"
              @click="ok('createTask')">添加
      </Button>
      <Button v-if="viewDialogShow" type="success" style="width: 80px; height:30px;" shape="circle"
              @click="ok('createTask')">保存
      </Button>
      <!--<Button type="ghost"  style="width: 80px; height:30px;"  shape="circle" @click="cancel">取消</Button>-->
    </div>
  </Modal>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import { initProjectVersions, initTaskForm, taskValidateRules } from './ProjectTaskCreateDialog'
  import FormItem from '../../../../node_modules/iview/src/components/form/form-item.vue'
  import { Window, WindowInstaller} from  '@progress/kendo-window-vue-wrapper'

  export default {
    name: 'ProjectTaskCreateDialog',
    props: {
      taskID: {
        type: Number,
        default: 0
      }
    },
    components: {
      FormItem,
      Window
    },
    data () {
      return {
        sourceProject: [],
//        projectMember: [],
        projectVersions: [],
        formItem: {
          id: this.taskID,
          Title: '',
          Owner: 0,
          Priority: '3',
          DeadLine: '',
          WorkHours: 8,
          Description: '',
          ProjectID: [],
          childTask: {
            index: 0,
            items: [
              {}
            ]
          },
          attachments: {
            defaultList: [
              {
                name: 'a42bdcc1178e62b4694c830f028db5c0',
                url: 'https://o5wwk8baw.qnssl.com/a42bdcc1178e62b4694c830f028db5c0/avatar'
              },
              {
                name: 'bc7521e033abdd1e92222d733590f104',
                url: 'https://o5wwk8baw.qnssl.com/bc7521e033abdd1e92222d733590f104/avatar'
              }
            ],
            imgName: '',
            visible: false,
            uploadList: []
          }
        },
        ruleCustom: {
          ...taskValidateRules
        }
      }

    },
    computed: {
      ...mapGetters('projectglobal', ['createDialogShow', 'viewDialogShow', 'projectVersion']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight-100
      },
      dialogShow: function () {
        return (this.createDialogShow || this.viewDialogShow)
      },
      task: function () {
        if (this.createDialogShow) {
          return 0
        }
        else {
          return this.taskID
        }
      },

      projectMembers: function () {
        let project = this.formItem.ProjectID[0]
        let result = []
        for (let i = 0; i < this.sourceProject.length; i++) {
          if (this.sourceProject[i].id === project) {
            result = this.sourceProject[i].Members
          }
        }
        return result
      }
    },
    methods:
      {
        ...mapMutations('projectglobal', ['setCreateDialogShow', 'setViewDialogShow', 'setObjectChange']),
        ...mapMutations('task', ['setTaskChange']),

        ok (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {
              if (this.createDialogShow) {
                this.$axios.post('/api/project/' + this.formItem.ProjectID[0] + '/version/' + this.formItem.ProjectID[1] + '/project_tasks', this.formItem).then(response => {
                  this.setTaskChange(true)
                  }, response => {
                  this.setTaskChange(true)

                })
              }
              if (this.viewDialogShow) {
                this.$axios.put('/api/project/task/' + this.taskID + '/', this.formItem).then(response => {
                  this.setTaskChange(true)
                }, response => {
                  this.setTaskChange(true)
                })
              }
              this.setCreateDialogShow(false)
              this.setViewDialogShow(false)
            }
          })
        },
        cancel () {
//          this.$Message.info('Clicked cancel')
          this.setCreateDialogShow(false)
          this.setViewDialogShow(false)
        },
        handleAdd () {
          this.formItem.childTask.index++
          this.formItem.childTask.items.push({
            value: '',
            index: this.formItem.childTask.index,
            status: 0,
            active: 1
          })
//          console.log(this.formItem)
        },
        handleRemove (index) {
          this.formItem.childTask.items[index].active = 0

        },
        handleView (name) {
          this.formItem.attachments.imgName = name
          this.formItem.attachments.visible = true
        },
        handleSuccess (res, file) {
          file.url = 'https://o5wwk8baw.qnssl.com/7eb99afb9d5f317c912f08b5212fd69a/avatar'
          file.name = '7eb99afb9d5f317c912f08b5212fd69a'
        },
        handleFormatError (file) {
          this.$Notice.warning({
            title: 'The file format is incorrect',
            desc: 'File format of ' + file.name + ' is incorrect, please select jpg or png.'
          })
        },
        handleMaxSize (file) {
          this.$Notice.warning({
            title: 'Exceeding file size limit',
            desc: 'File  ' + file.name + ' is too large, no more than 2M.'
          })
        },
        handleBeforeUpload () {
        },
        onProjectChange (value, selectedData) {
          let project = value[0]
          for (let i = 0; i < this.sourceProject.length; i++) {
            if (this.sourceProject[i].id === project) {
              this.projectMember = this.sourceProject[i].Members
            }
          }
        },

        loadProjectInfo: function () {
          this.$axios.get('/api/project/list?extinfo=1&home=1').then(response => {

            let tempData = response.data.result
            this.sourceProject = tempData
            this.projectVersions = initProjectVersions(tempData)
          }, response => {
            // error callback
          })
        },

        initTaskForm: function () {
          this.formItem.childTask.items = []
          this.formItem.id = this.task
          let defaultTask = this.formItem

          if (this.formItem.id !== 0) {
            let initPromise = initTaskForm(this.taskID)
            initPromise.then(function (initData) {
              defaultTask.Title = initData.Title
              defaultTask.Owner = parseInt(initData.Owner)
              defaultTask.Priority = initData.Priority + ''
              defaultTask.DeadLine = initData.DeadLine
              defaultTask.Description = initData.Description
              defaultTask.WorkHours = parseInt(initData.WorkHours)
              defaultTask.ProjectID = [initData.ProjectID, initData.Version]
              for (let i = 0; i < initData.Child.length; i++) {
                defaultTask.childTask.index = defaultTask.childTask.index + 1
                let temp = {}
                temp.value = initData.Child[i].Title
                temp.index = i + 1
                temp.status = initData.Child[i].Status
                temp.active = initData.Child[i].IsActive
                temp.id = initData.Child[i].id
                defaultTask.childTask.items.push(temp)
              }
              if (initData.Child.length === 0) {
                defaultTask.childTask.items = []
              }

            })
          }
          else {
            defaultTask.Title = ''
            defaultTask.Owner = 0
            defaultTask.Priority = '3'
            defaultTask.DeadLine = ''
            defaultTask.Desc = ''
            defaultTask.WorkHours = 8
            defaultTask.ProjectID = []
            defaultTask.childTask.items = []
          }
        }
      },
    created () {
      this.loadProjectInfo()
    },
    mounted () {
//      this.formItem.attachments.uploadList = this.$refs.upload.fileList
    },
    watch: {

      task: function () {
        this.initTaskForm()
     },

      viewDialogShow: function ( value) {
        if (value)
        {
          this.initTaskForm()
        }
      },

      formItem: function () {
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .demo-upload-list {
    display: inline-block;
    width: 60px;
    height: 60px;
    text-align: center;
    line-height: 60px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    position: relative;
    box-shadow: 0 1px 1px rgba(0, 0, 0, .2);
    margin-right: 4px;
  }

  .demo-upload-list img {
    width: 100%;
    height: 100%;
  }

  .demo-upload-list-cover {
    display: none;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, .6);
  }

  .demo-upload-list:hover .demo-upload-list-cover {
    display: block;
  }

  .demo-upload-list-cover i {
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    margin: 0 2px;
  }
</style>
