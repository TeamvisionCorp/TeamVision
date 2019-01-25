<template>
  <Modal :value="dialogShow" :title="dialogTitle" :width="700" @on-cancel="cancel" :styles="{bottom:'20px',top: '50px'}">
    <div :style="'height:' + containerHeight + 'px;overflow-y: scroll;overflow-x: hidden'">
      <Form ref="createFortesting" :model="formItem" :label-width="80" :rules="ruleCustom">
        <FormItem label="项目" prop="ProjectVersion">
          <Cascader v-model="formItem.ProjectVersion" :data="projectVersions" @on-change="onProjectChange"
                    :filterable="true"></Cascader>
        </FormItem>
        <FormItem label="主题" prop="Topic">
          <Input v-model="formItem.Topic" placeholder="提测主题"/>
        </FormItem>
        <FormItem label="代码仓库" prop="CodeRepertory">
          <Input v-model="formItem.CodeRepertory" placeholder="代码仓库地址"/>
        </FormItem>
        <FormItem label="分支" prop="Branch">
          <Input v-model="formItem.Branch" placeholder="代码分支"/>
        </FormItem>
        <FormItem label="提测内容:" prop="TestingFeature">
          <Table :columns="columns" :data="contentData" :show-header="false" disabled-hover>
            <template slot-scope="{ row, index }" slot="name">
              <Input  @on-blur="handleSave(row,index)" v-model="row.name" type="text" placeholder="请输入提测内容，点击+，添加更多提测内容"  />
            </template>

            <template slot-scope="{ row, index }" slot="action">
              <div v-if="index === contentData.length-1">
                <Icon @click="handleAdd(row, index)" type="ios-add-circle" style="color:#32be77;"  :size="18" class="cursor-hand"/>
              </div>
            </template>
          </Table>
          <!--<vue-editor v-model="formItem.TestingFeature" :editorToolbar="editorToolBar" @text-change="commitContentChange" placeholder="提测内容"></vue-editor>-->
        </FormItem>
        <FormItem>

        </FormItem>
        <FormItem label="测试建议:" prop="TestingAdvice">
          <vue-editor v-model="formItem.TestingAdvice" :editorToolbar="editorToolBar" placeholder="测试建议"></vue-editor>
        </FormItem>
        <div style="border-top: 1px solid rgba(0,0,0,.1);margin-top: 20px;"></div>
        <div style="font-size: 14px;padding-top: 5px;color:#495060">
          <Icon type="android-attach" :size="14"></Icon>
          附件
        </div>
        <FormItem>
          <div class="demo-upload-list" :key="index" v-for="(item,index) in formItem.attachments.uploadList">
            <div v-if="item.status === 'finished'">
              <div>{{ item.name }}</div>
              <div class="demo-upload-list-cover">
                <a :href="item.url">
                  <Icon type="ios-cloud-download-outline"/>
                </a>
                <Icon type="ios-trash-outline" @click.native="handleRemove(item)"></Icon>
              </div>
            </div>
            <div v-else>
              <Progress v-if="item.showProgress" :percent="item.percentage" hide-info></Progress>
            </div>
          </div>
          <Upload
            ref="upload"
            :show-upload-list="false"
            :default-file-list="formItem.attachments.defaultList"
            :on-success="handleSuccess"
            :format="['jpg','jpeg','png','pdf','txt','sql','docx','doc','xlsx']"
            :max-size="10240"
            :on-format-error="handleFormatError"
            :on-exceeded-size="handleMaxSize"
            :before-upload="handleBeforeUpload"
            multiple
            type="drag"
            action="/api/project/fortesting/upload_files"
            style="display: inline-block;width:100px;">
            <div style="width: 100px;height:100px;line-height: 100px;">
              <Icon type="ios-camera-outline" :size="20"/>
            </div>
          </Upload>
        </FormItem>
      </Form>
    </div>
    <div slot="footer">
      <Button v-if="createDialogShow" type="success" style="width: 80px; height:30px;" shape="circle"
              @click="ok('createFortesting')">添加
      </Button>
      <Button v-if="viewDialogShow" type="success" style="width: 80px; height:30px;" shape="circle"
              @click="ok('createFortesting')">保存
      </Button>
      <!--<Button type="ghost"  style="width: 80px; height:30px;"  shape="circle" @click="cancel">取消</Button>-->
    </div>
  </Modal>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import { initFortestingForm, initProjectVersions, fortestingValidateRules } from './ProjectFortestingCreateDialog'
  import FormItem from '../../../../node_modules/iview/src/components/form/form-item.vue'
  import { VueEditor } from 'vue2-editor'

  export default {
    name: 'ProjectFortestingCreateDialog',
    props: {
      fortestingID: {
        type: Number,
        default: 0
      }
    },
    data () {
      return {
        content: '',
        defaultProjectID: [],
        sourceProject: [],
        editorToolBar: [
          ['bold', 'italic', 'underline'],
          [{'list': 'ordered'}, {'list': 'bullet'}],[{ 'color': [] }, { 'background': [] }],
        ],
        projectModules: [],
        projectVersions: [],
        dialogTitle: '添加提测',
        formItem: {
          Topic: '',
          ProjectModuleID: '0',
          ProjectID: 0,
          VersionID: 0,
          CodeRepertory: '',
          Branch: '',
          TestingAdvice: '',
          TestingFeature: '',
          ProjectVersion: [],
          attachments: {
            defaultList: [],
            imgName: '',
            visible: false,
            uploadList: []
          }
        },
        columns: [
          {
            title: '',
            slot: 'name',
          },
          {
            title: '',
            slot: 'action',
            width: 100
          }
        ],
        contentData: [{name: ''}
        ],
        editIndex: 0,  // 当前聚焦的输入框的行数
        editName: '',  // 第一列输入框，当然聚焦的输入框的输入内容，与 data 分离避免重构的闪烁
        ruleCustom: {
          ...fortestingValidateRules
        }
      }

    },
    computed: {
      ...mapGetters('projectglobal', ['createDialogShow', 'viewDialogShow', 'projectVersion', 'project']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight-100
      },

      dialogShow: function () {
        return (this.createDialogShow || this.viewDialogShow)
      },

      fortesting: function () {
        if (this.createDialogShow) {
          return 0
        }
        else {
          return this.fortestingID
        }
      }
    },
    methods:
      {
        ...mapMutations('projectglobal', ['setCreateDialogShow', 'setViewDialogShow', 'setObjectChange']),

        ok (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {
              if (this.createDialogShow) {
                this.$axios.post('/api/project/' + this.formItem.ProjectID + '/version/' + this.formItem.VersionID + '/fortestings', this.formItem).then(response => {
                  this.setObjectChange(true)
                }, response => {

                })
              }
              if (this.viewDialogShow) {
                this.$axios.put('/api/project/fortesting/' + this.fortestingID + '/', this.formItem).then(response => {
                  this.setObjectChange(true)

                }, response => {

                })
                this.updateAttachments()
              }
              this.setCreateDialogShow(false)
              this.setViewDialogShow(false)
              this.setObjectChange(true)
            }
          })
        },
        cancel () {
          this.setCreateDialogShow(false)
          this.setViewDialogShow(false)
        },
        handleView (name) {
          this.formItem.attachments.imgName = name
          this.formItem.attachments.visible = true
        },
        handleRemove (file) {
          const fileList = this.formItem.attachments.uploadList
          this.formItem.attachments.uploadList.splice(fileList.indexOf(file), 1)
          this.removeFile(file.id)
          this.updateAttachments()
        },
        handleSuccess (res, file) {
          file.url = res.result.url
          file.id = res.result.file_id
          this.formItem.attachments.uploadList = this.$refs.upload.fileList
        },
        handleFormatError (file) {
          this.$Message.warning({
            content: '文件格式不正确,格式：\'jpg\',\'jpeg\',\'png\',\'pdf\',\'txt\',\'sql\',\'docx\',\'doc\',\'xlsx\'',
            duration: 10,
            closable: true
          })
        },
        handleMaxSize (file) {
          this.$Message.warning({
            content: '文件大小超过10M限制',
            duration: 10,
            closable: true
          })
        },
        handleBeforeUpload () {
        },
        onProjectChange (value, selectedData) {
          let project = value[0]
          this.formItem.ProjectID = value[0]
          this.formItem.VersionID = value[1]
          this.loadProjectModules(project)
        },
        commitContentChange: function (delta, oldDelta, source) {
        },
        updateAttachments: function () {
          let result = ''
          for (let i = 0; i < this.formItem.attachments.uploadList.length; i++) {
            result = this.formItem.attachments.uploadList[i].id + ',' + result
          }
          this.$axios.patch('/api/project/fortesting/' + this.fortestingID + '/', {'Attachment': result}).then(response => {

          }, response => {

          })

        },

        handleAdd (row, index) {
          this.contentData.push({name: ''})
        },
        handleSave (row,index) {
          if (row.name.trim() !== '') {
          this.formItem.TestingFeature = this.formItem.TestingFeature + row.name + '{;}'
          this.contentData[index].name = row.name
          }
        },

        removeFile: function (file_id) {
          this.$axios.delete('/api/project/fortesting/delete_file/' + file_id).then(response => {

          }, response => {

          })
        },

        loadProjectModules: function (project) {
          this.$axios.get('/api/project/' + project + '/modules').then(response => {
            let tempData = response.data.result
            this.projectModules = tempData
          }, response => {
            // error callback
          })
        },
        loadMyProjectList: function () {
          this.$axios.get('/api/project/list?extinfo=1&home=1').then(response => {
            let tempData = response.data.result
            this.sourceProject = tempData
            this.projectVersions = initProjectVersions(tempData)
          }, response => {
            // error callback
          })
        },

        loadForTesting: function () {
          this.formItem.id = this.fortesting
          this.contentData = [{name: ''}]
          let defaultTask = this.formItem
          let defaultProject = this.defaultProjectID
          let defaultTesingFeature = this.contentData

          if (this.formItem.id !== 0) {
            let initPromise = initFortestingForm(this.fortesting)
            initPromise.then(function (initData) {
              defaultTask.Topic = initData.Topic
              defaultTask.Branch = initData.Branch
              defaultTask.CodeRepertory = initData.CodeRepertory
              for (let i=0;i<initData.FortestingFeature.length;i++) {
                if (initData.FortestingFeature[i].trim() !== '') {
                  let tempData = {}
                  tempData['name'] = initData.FortestingFeature[i]
                  defaultTesingFeature.push(tempData)
                }
              }
              defaultTask.TestingAdvice = initData.TestingAdvice.replace('div','p')
              defaultTask.ProjectModuleID = initData.ProjectModuleID
              defaultTask.ProjectVersion = [initData.ProjectID, initData.VersionID]
              defaultTask.ProjectID = initData.ProjectID
              defaultTask.VersionID = initData.VersionID
              defaultTask.attachments.defaultList = initData.Attachments
              defaultTask.attachments.uploadList = initData.Attachments
              defaultProject.push(initData.ProjectID)
            })
          }
          else {
            defaultTask.Topic = ''
            defaultTask.Branch = ''
            defaultTask.CodeRepertory = ''
            defaultTask.TestingFeature = ''
            defaultTask.TestingAdvice = ''
            defaultTask.ProjectModuleID = 0
            defaultTask.ProjectVersion = []
            defaultTask.attachments.defaultList = []
            defaultTask.attachments.uploadList = []
          }
        }
      },
    created () {
      this.loadMyProjectList()
    },
    mounted () {
      this.formItem.attachments.uploadList = this.$refs.upload.fileList
    },
    watch: {
      fortesting: function () {
        this.loadForTesting()
      },

      createDialogShow: function (value) {
         if (value===true)
         {
           this.dialogTitle = '添加提测'
         }
      },
      viewDialogShow: function (value) {
        if (value === true)
        {
          this.dialogTitle = '编辑提测'
          this.loadForTesting()
        }
      }

    },
    components: {
      FormItem,
      VueEditor
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .demo-upload-list {
    display: inline-block;
    width: 100px;
    height: 100px;
    text-align: center;
    margin: 5px;
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
