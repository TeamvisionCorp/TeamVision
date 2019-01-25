<template>
  <div style="margin: -16px;" class="issue-detail">
    <div class="issue-title">
      <Button v-if="issueDetail.Status===5"  style="margin-right: 10px;"  @click="onResloveIssue" size="small" type="success" shape="circle" icon="ios-construct" ghost>解决</Button>
      <Button v-if="issueDetail.Status===2"  style="margin-right: 10px;"  @click="onResloveIssue" size="small" type="success" shape="circle" icon="ios-construct" ghost>解决</Button>
      <Button v-if="issueDetail.Status!==3" style="margin-right: 10px;" @click="onCloseIssue" size="small" type="warning" shape="circle" icon="md-checkmark-circle-outline" ghost>关闭</Button>
      <Button v-if="issueDetail.Status === 3"  style="margin-right: 10px;" @click="onReOpenIssue" size="small" type="error" shape="circle" icon="md-redo" ghost>重新打开</Button>
      <Button v-if="issueDetail.Status === 4"  style="margin-right: 10px;" @click="onReOpenIssue" size="small" type="error" shape="circle" icon="md-redo" ghost>重新打开</Button>
    </div>
    <Divider style="margin:0px"/>
    <div class="issue-detail-body">
      <div class="issue-detail-summary">
        <div>
          <span class="issue-detail-id">#{{ issueDetail.id }}</span>
          <span class="issue-default-title">{{ issueDetail.default_title }}</span>
          <span class="issue-detail-title">
              <label-editor-input  @updateValue="updateIssueTitle" placeHolder="问题标题" :displayText="issueDetail.Title"></label-editor-input>
            </span>
        </div>
        <div class="issue-detail-creation">
          <span class="issue-detail-creator">{{ issueDetail.creator_name }} 创建于</span>
          <span class="issue-detail-createdate">{{ issueDetail.create_date }}</span>
          <span class="issue-detail-createdate">{{ issueDetail.update_date }} 更新</span>
        </div>
        <div class="issue-detail-topic">
          <Row>
            <i-col :span="6">
                   <span class="issue-detail-topic-content">
                      <span class="issue-detail-topic-field-name">状态</span>
                      <i :class="'fa ' + issueDetail.status_name.Label + ' ' + issueDetail.status_name.LabelStyle "></i>
                      <span>{{ issueDetail.status_name.Name }}</span>
                   </span>
            </i-col>
            <i-col :span="6">
                    <span class="issue-detail-topic-content">
                      <span class="issue-detail-topic-field-name">解决结果</span>
                     <i
                       :class="'fa ' + issueDetail.solution_name.Label + ' ' + issueDetail.solution_name.LabelStyle "></i>
                      <span>{{ issueDetail.solution_name.Name }}</span>
                   </span>
            </i-col>
            <i-col :span="6">
                    <span class="issue-detail-topic-content">
                      <span class="issue-detail-topic-field-name">严重性</span>
                       <i
                         :class="'fa ' + issueDetail.severity_name.Label + ' ' + issueDetail.severity_name.LabelStyle "></i>
                      <span>
                        <Dropdown @on-click="onFieldItemClick">
        <a href="javascript:void(0)">
          <span ref="Severity">{{ issueDetail.severity_name.Name }}</span>
            <Icon type="ios-arrow-down"></Icon>
        </a>
        <DropdownMenu slot="list">
            <DropdownItem v-for="item in issueSeverity" :selected="item.id === issueDetail.Severity" :name="item.Value + ',' + item.Name + ',' + 'Severity'" :key="item.Value">{{ item.Name }}</DropdownItem>
        </DropdownMenu>
    </Dropdown>
                      </span>

                   </span>
            </i-col>
            <i-col :span="6">
                    <span class="issue-detail-topic-content">
                      <span class="issue-detail-topic-field-name">优先级</span>
                      <i class="fa fa-fire issue-status-reopen"></i>
                      <span>
                        <Dropdown  @on-click="onFieldItemClick">
        <a href="javascript:void(0)">
          <span ref="Priority">{{ issueDetail.priority_name }}</span>
            <Icon type="ios-arrow-down"></Icon>
        </a>
        <DropdownMenu slot="list">
            <DropdownItem v-for="item in issuePriority" :selected="item.id === issueDetail.Priority" :name="item.Value + ',' + item.Name + ',' + 'Priority'" :key="item.Value">{{ item.Name }}</DropdownItem>
        </DropdownMenu>
    </Dropdown>
                      </span>
                   </span>
            </i-col>
          </Row>
        </div>
      </div>
      <Divider style="margin:0px"/>
      <div class="issue-detail-editor">
        <div class="issue-detail-desc">
          <div class="issue-detail-desc-title">
            <i class="fa fa-sticky-note"></i>
            描述：
          </div>
            <div class="issue-detail-desc-content-veiw">
              <label-editor-vue-editor placeHolder="问题描述" @updateValue="updateIssueDesc" :displayText="issueDetail.Desc"></label-editor-vue-editor>
            </div>
        </div>
        <Divider style="margin:0px"/>
        <div class="issue-detail-option">
          <Row style="height: 50px;">
            <i-col :span="8" class="issue-detail-field-content">
              <Dropdown  @on-click="onFieldItemClick">
                <span>
                   <i class="fa fa-hand-o-right"></i> 经办人：
                </span>
                <a href="javascript:void(0)">
                  <span ref="Processor">{{ issueDetail.processor_name }}</span>
                  <Icon type="ios-arrow-down"></Icon>
                </a>
                <DropdownMenu slot="list">
                  <DropdownItem v-for="item in projectMembers" :selected="item.id === issueDetail.Processor" :name="item.id + ',' + item.name + ',' + 'Processor'" :key="item.id">{{ item.name }}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </i-col>
            <i-col :span="8" class="issue-detail-field-content">
              <Dropdown  @on-click="onFieldItemClick">
                <span ref="Team">
                   <i class="fa fa-hand-o-right"></i> 团队：
                </span>
                <a href="javascript:void(0)">
                  <span ref="Team">{{ issueDetail.team_name }}</span>
                  <Icon type="ios-arrow-down"></Icon>
                </a>
                <DropdownMenu slot="list">
                  <DropdownItem v-for="item in projectTeams" :selected="item.id === issueDetail.Team" :name="item.id + ',' + item.Name + ',' + 'Team'" :key="item.Value">{{ item.Name }}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </i-col>
            <i-col :span="8" class="issue-detail-field-content">
              <Dropdown  @on-click="onFieldItemClick">
                <span>
                   <i class="fa fa-cube"></i> 模块：
                </span>
                <a href="javascript:void(0)">
                  <span ref="Module"> {{ issueDetail.module_name }}</span>
                  <Icon type="ios-arrow-down"></Icon>
                </a>
                <DropdownMenu slot="list">
                  <DropdownItem v-for="item in projectModules" :selected="item.id === issueDetail.Module" :name="item.id + ',' + item.Name + ',' + 'Module'" :key="item.id">{{ item.Name }}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </i-col>
          </Row>
          <Row style="height: 50px;">
            <i-col :span="8" class="issue-detail-field-content">
              <Dropdown  @on-click="onFieldItemClick">
                <span>
                   <i class="fa fa-code-fork"></i> 版本：
                </span>
                <a href="javascript:void(0)">
                  <span ref="Version">{{ issueDetail.version_name }}</span>
                  <Icon type="ios-arrow-down"></Icon>
                </a>
                <DropdownMenu slot="list">
                  <DropdownItem v-for="item in projectVersions" :selected="item.id === issueDetail.Version" :name="item.id + ',' + item.VVersion + ',' + 'Version'" :key="item.id">{{ item.VVersion }}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </i-col>
            <i-col :span="8" class="issue-detail-field-content">
              <Dropdown  @on-click="onFieldItemClick">

                <span>
                   <i class="fa fa-chain"></i> 问题分类：
                </span>
                <a href="javascript:void(0)">
                 <span ref="IssueCategory">{{ issueDetail.category_name }}</span>
                  <Icon type="ios-arrow-down"></Icon>
                </a>
                <DropdownMenu slot="list">
                  <DropdownItem v-for="item in issueCategories" :selected="item.id === issueDetail.IssueCategory" :name="item.Value + ',' + item.Name + ',' + 'IssueCategory'" :key="item.Value">{{ item.Name }}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </i-col>
            <i-col :span="8" class="issue-detail-field-content">
              <Dropdown  @on-click="onFieldItemClick">
                <span>
                   <i class="fa fa-leaf"></i> 项目阶段：
                </span>
                <a href="javascript:void(0)">
                  <span ref="ProjectPhase"> {{ issueDetail.project_phrase_name }}</span>
                  <Icon type="ios-arrow-down"></Icon>
                </a>
                <DropdownMenu slot="list">
                  <DropdownItem v-for="item in issueProjectPhrase" :selected="item.id === issueDetail.ProjectPhase" :name="item.Value + ',' + item.Name + ',' + 'ProjectPhase'" :key="item.Value">{{ item.Name }}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </i-col>
          </Row>
          <Row>
            <i-col :span="8" class="issue-detail-field-content">
              <Dropdown  @on-click="onFieldItemClick">
                <span>
                   <i class="fa fa-sticky-note"></i> 系统：
                </span>
                <a href="javascript:void(0)">
                 <span ref="DeviceOS"> {{ issueDetail.os_name }}</span>
                  <Icon type="ios-arrow-down"></Icon>
                </a>
                <DropdownMenu slot="list">
                  <DropdownItem v-for="item in DeviceOS" :selected="item.id === issueDetail.DeviceOS" :name="item.Value + ',' + item.Name + ',' + 'DeviceOS'" :key="item.Value">{{ item.Name }}</DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </i-col>
          </Row>
        </div>
        <Divider style="margin:0px"/>
        <div class="issue-detail-attachment">
          <Row>
            <i-col :span="18">
              <span style="color: #b2b2b2;font-size: 14px;"><Icon type="ios-attach" :size="20"/>附件：</span>
            </i-col>
            <i-col :span="6">
              <span @click="uploadIssueAttachment"><Button icon="md-cloud-upload" shape="circle" size="small">上传</Button></span>
            </i-col>
          </Row>
          <div style="padding-top: 20px;">
            <Row  v-for="attachment in issueDetail.attachments_detail"  :key="attachment.id" class="attachment-item">
              <i-col :span="18">
                <span class="cursor-hand" @click="onViewAttachment(attachment.FileName,attachment.id,attachment.FileSuffixes)"><Icon type="ios-attach" :size="15"/>{{ attachment.FileName }}</span>
              </i-col>
              <i-col :span="6">
                <a :href="'/project/issue/download/' + attachment.id"><Icon type="ios-cloud-download" :size="20" /></a>
                <span class="cursor-hand" @click="delectAttachment(attachment.id,attachment.FileName)"><Icon type="ios-trash" :size="20"/></span>
                <span style="padding-left: 30px; color:#b2b2b2">
                  <Time :time="attachment.CreationTimeFormat" />
                </span>
              </i-col>
            </Row>

          </div>

        </div>
        <Divider style="margin:0px"/>
        <div class="issue-detail-comments">
          <div style="font-size: 15px;margin-bottom: 15px;"><Icon type="ios-megaphone" :size="15"/> 问题动态</div>
          <div style="padding-left: 20px;padding-bottom: 40px;">
            <Timeline>
              <TimelineItem v-for="item in issueActivities" :key="item.id" color="#3b73af">
                <Icon  :size="20" type="md-add-circle" slot="dot"></Icon>
                <span style="font-size: 15px;">
                  {{ item.creator_name }}  {{ item.action_flag_name }} {{ item.action_type_name }} {{ item.Message }} [{{ item.FieldDesc }}]
                  <span style="text-decoration: line-through;" v-html="item.OldValue">{{ item.OldValue }}</span>
                  <span v-html="item.NewValue"></span>
                </span>
                <span style="float: right;padding-right: 20px;">{{ item.create_date }}</span>
              </TimelineItem>
            </Timeline>
          </div>
        </div>
      </div>
      <div class="issue-comments-input">
        <Input search enter-button="发布"  @on-search="onAddComments" size="large" placeholder="输入内容，回车发布备注信息" />
      </div>
    </div>
    <Modal v-model="viewAttachment.showDialog" fullscreen footer-hide :title="viewAttachment.fileName">
      <div v-if="viewAttachment.isPicture!==true">
        <Alert type="error" show-icon>
          <span slot="desc">
            不支持非图片类文件的预览，请下载这个文件！
        </span>
        </Alert>
        </div>
      <div v-if="viewAttachment.isPicture">
        <img :src="'http://localhost:8000/project/issue/download/' + viewAttachment.fileID "/>
      </div>
    </Modal>

    <Modal v-model="showUploadAttachmentDialog" title="附件上传" @on-ok="onPatchIssueAttachment">
      <Tabs>
        <TabPane label="本地上传">
          <Upload ref="upload" multiple type="drag" paste action="/api/project/issue/attachments"
                  :on-success="handleSuccess"
                  :on-remove="handleRemove"
                  :format="[]"
                  :max-size="10240"
                  :default-file-list="defaultList"
                  :on-format-error="handleFormatError"
                  :on-exceeded-size="handleMaxSize">
            <div style="padding: 20px 0">
              <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
              <p>点击，拖拽，粘贴上传附件</p>
            </div>
          </Upload>
        </TabPane>
        <TabPane label="扫码上传">
          <img :src="'/api/common/toolkit/qrcode?content=' +qrcodeContent " style="height: 100px;width: 100px;"/>
        </TabPane>
      </Tabs>
    </Modal>

    <Modal v-model="resloveIssueDialog.isShow" :title="resloveIssueDialog.title" @on-ok="resloveIssueResult">
      <Form ref="resloveIssue" :model="formItem" :label-width="80">
        <FormItem v-if="resloveIssueDialog.dialogType === 1" label="解决结果" prop="ResloveResult">
          <Select v-model="formItem.ResloveResult" :filterable="true">
            <Option v-for="item in issueResolvedResult" :key="item.Value" :value="item.Value">{{ item.Name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="描述" prop="Desc">
          <vue-editor v-model="formItem.Desc" :editorToolbar="editorToolBar"  placeholder="问题描述"></vue-editor>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>

<script>
import labelEditorInput from '../../../components/common/LabelEditor-Input.vue'
import labelEditorSelect from '../../../components/common/LabelEditor-Select.vue'
import labelEditorVueEditor from '../../../components/common/LabelEditor-VUEEditor.vue'
import { VueEditor } from 'vue2-editor'
import ICol from "../../../../node_modules/iview/src/components/grid/col.vue";
import {mapGetters, mapMutations} from 'vuex'

  export default {
    name: 'ProjectIssueDetail',
    props: ['issueID'],
    data() {
      return {
        issueDetail: {},
        projectVersions: [],
        projectMembers: [],
        projectTeams: [],
        projectModules: [],
        issueSeverity: [],
        issueProjectPhrase: [],
        issueCategories: [],
        DeviceOS: [],
        issuePriority: [],
        issueResolvedResult: [],
        issueActivities: [],
        viewAttachment: {
          isPicture: false,
          showDialog: false,
          fileName: '',
          fileID: 0
        },
        editorToolBar: [
          ['bold', 'italic', 'underline'],
          [{'list': 'ordered'}, {'list': 'bullet'}],[{ 'color': [] }, { 'background': [] }],
        ],
        showUploadAttachmentDialog: false,
        uploadList: [],
        defaultList: [],
        resloveIssueDialog: {
          isShow: false,
          title: '',
          dialogType: 0
        },
        issueComments: {
          Message: '',
          ActionFlag: 1,
          ActionType: 2,
          Issue: 0,
          OldValue: '',
          NewValue: '',
          FieldName: ''
        },
        formItem: {
          ResloveResult: 1,
          Desc: ''
        }
      }
    },

    computed: {
      ...mapGetters(['appBodyHeight', 'userInfo']),
      qrcodeContent: function () {
        return 'http://' + window.location.host + '/project/issue/' + this.issueID + '/mobile/upload'
      }
    },

    methods: {

      ...mapMutations('issue', ['setIssueChange']),

      loadIssueDetail: function (issueID) {
        this.$axios.get('/api/project/issue/' + issueID).then(response => {
          this.issueDetail = response.data.result
          this.loadIssueProjectModules(this.issueDetail.Project)
          this.loadProject(this.issueDetail.Project)
        }, response => {
        })
      },

      handleSuccess (res, file, fileList) {
        file.url = res.result.url
        file.id = res.result.file_id
        this.uploadList.push(file.id)
      },

      handleRemove (file, fileList) {
        this.uploadList = fileList
        console.log(this.uploadList)
      },

      handleFormatError (file) {
        this.$Message.warning({
          content: '文件格式不正确,格式：\'jpg\',\'jpeg\',\'png\'',
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

      uploadIssueAttachment: function () {
        this.showUploadAttachmentDialog = true
      },

      delectAttachment: function (fileID,fileName) {
          this.$Modal.confirm({
            title: '附件删除确认',
            content: '即将删除附件' + fileName,
            onOk: () => {
              this.$axios.delete('/api/project/issue/' + this.issueDetail.id + '/attachment/' + fileID).then(response => {
                this.loadIssueDetail(this.issueDetail.id)

              }, response => {
              })
            },
            onCancel: () => {
            }
          })
      },

      onPatchIssueAttachment: function () {
        let paras = {}
        paras['uploadList'] = this.uploadList
        this.$axios.patch('/api/project/issue/' + this.issueDetail.id + '/attachment/0',paras).then(response => {
          this.$Message.success({
            content: '文件上传成功',
            duration: 10,
            closable: true
          })
          this.uploadList = []
          this.loadIssueDetail(this.issueDetail.id)
        }, response => {
          this.uploadList = []
        })
      },

      onResloveIssue: function () {
        this.resloveIssueDialog.isShow = true
        this.resloveIssueDialog.title = '解决问题'
        this.resloveIssueDialog.dialogType = 1
      },

      onCloseIssue: function () {
        this.resloveIssueDialog.isShow = true
        this.resloveIssueDialog.title = '关闭问题'
        this.resloveIssueDialog.dialogType = 2
      },

      onReOpenIssue: function () {
        this.resloveIssueDialog.isShow = true
        this.resloveIssueDialog.title = '重新打开问题'
        this.resloveIssueDialog.dialogType = 3
      },

      resloveIssueResult: function () {
        this.formItem['operation'] = this.resloveIssueDialog.dialogType
        this.$axios.post('/api/project/issue/' + this.issueDetail.id,this.formItem).then(response => {
          this.setIssueChange(true)
          this.loadIssueDetail(this.issueID)
          this.loadIssueActivities(this.issueID)
        }, response => {
        })

      },

      loadProject: function (projectID) {
        this.$axios.get('/api/project/' + projectID + '/detail?extinfo=1').then(response => {
          this.projectVersions = response.data.result.Versions
          this.projectMembers = response.data.result.Members
        }, response => {
        })
      },

      updateIssueTitle: function (value) {
        if (value.trim() !== this.issueDetail.Title.trim())
        {
          this.updateIssueInputField(this.issueDetail.Title.trim(),value.trim(),'Title')
        }
      },

      updateIssueDesc: function (value) {
        if (value.trim() !== this.issueDetail.Desc.trim())
        {
          this.updateIssueInputField(this.issueDetail.Desc.trim(),value.trim(),'Desc')
        }
      },

      updateIssueInputField: function (oldValue,newValue,fieldName) {
        this.issueComments.OldValue = oldValue
        this.issueDetail[fieldName] = newValue
        this.issueComments.Message = '属性'
        this.issueComments.Issue = this.issueID
        this.issueComments.Creator = this.userInfo.id
        this.issueComments.NewValue = newValue
        this.issueComments.FieldName = fieldName
        this.issueComments.ActionFlag = 2
        this.issueComments.ActionType = 1
        this.updateIssueProperty(fieldName, newValue)
      },

      loadMyTeams: function () {
        this.$axios.get('/api/common/teams/my').then(response => {
          this.projectTeams = response.data.result
        }, response => {
        })
      },

      loadIssueSeverity: function () {
        this.$axios.get('/api/project/issue/severities').then(response => {
          this.issueSeverity = response.data.result
        }, response => {
        })
      },

      loadIssueCategories: function () {
        this.$axios.get('/api/project/issue/categories').then(response => {
          this.issueCategories = response.data.result
        }, response => {
        })
      },

      loadIssueReslovedResult: function () {
        this.$axios.get('/api/project/issue/resolve_results').then(response => {
          this.issueResolvedResult = response.data.result
        }, response => {
        })
      },

      loadIssueProjectPhrase: function () {
        this.$axios.get('/api/project/issue/project_phrase').then(response => {
          this.issueProjectPhrase = response.data.result
        }, response => {
        })
      },
      loadIssueProjectModules: function (projectID) {

        this.$axios.get('/api/project/' + projectID + '/project_modules').then(response => {
          this.projectModules = response.data.result
        }, response => {
        })
      },

      loadIssueProjectPriority: function () {
        this.$axios.get('/api/project/issue/priority').then(response => {
          this.issuePriority = response.data.result
        }, response => {
        })
      },

      loadIssueOS: function () {
        this.$axios.get('/api/project/issue/os').then(response => {
          this.DeviceOS = response.data.result
        }, response => {
        })
      },

      loadIssueActivities: function (issueID) {
        this.$axios.get('/api/project/issue/' + issueID + '/activities').then(response => {
          this.issueActivities = response.data.result
        }, response => {
        })
      },

      onFieldItemClick: function (name) {
        let fieldItem = name.split(',')
        if (fieldItem.length === 3)
        {
          this.issueComments.OldValue = this.$refs[fieldItem[2]].innerHTML
          this.$refs[fieldItem[2]].innerHTML = fieldItem[1]
          this.issueDetail[fieldItem[2]] = parseInt(fieldItem[0])
          this.issueComments.Message = '属性'
          this.issueComments.Issue = this.issueID
          this.issueComments.Creator = this.userInfo.id
          this.issueComments.NewValue = fieldItem[1]
          this.issueComments.FieldName = fieldItem[2]
          this.issueComments.ActionFlag = 2
          this.issueComments.ActionType = 1
          this.updateIssueProperty(fieldItem[2],parseInt(fieldItem[0]))
        }
      },

      updateIssueProperty: function (fieldName,value) {
        let field = {}
        field[fieldName] = value
        this.$axios.patch('/api/project/issue/' + this.issueID, field).then(response => {
          this.$axios.post('/api/project/issue/' + this.issueID + '/activities', this.issueComments).then(response => {
            this.$Message.success({
              content: '问题成功更新。',
              duration: 10,
              closable: true
            })
            this.setIssueChange(true)
            this.loadIssueActivities(this.issueID)

          }, response => {
          })
        }, response => {
        })
      },

      onAddComments: function (value) {
        if (value.trim() !== '') {
          this.issueComments.Message = value
          this.issueComments.Issue = this.issueID
          this.issueComments.Creator = this.userInfo.id
          this.$axios.post('/api/project/issue/' + this.issueID + '/activities', this.issueComments).then(response => {
            this.loadIssueActivities(this.issueID)
          }, response => {
          })
        }
      },

      onViewAttachment: function (fileName,fileID,FileSuffixes) {
        this.viewAttachment.showDialog = true
        this.viewAttachment.fileName = fileName
        this.viewAttachment.fileID = fileID
        if (FileSuffixes === 'jpg' || FileSuffixes === 'jpeg' || FileSuffixes === 'png')
        {
          this.viewAttachment.isPicture = true
        } else {
          this.viewAttachment.isPicture = false
        }
      }
    },
    created () {
      this.loadIssueDetail(this.issueID)
      this.loadIssueSeverity()
      this.loadMyTeams()
      this.loadIssueProjectPriority()
      this.loadIssueOS()
      this.loadIssueProjectPhrase()
      this.loadIssueCategories()
      this.loadIssueReslovedResult()
    },
    watch: {
      issueID: function (value) {
        this.loadIssueDetail(value)
        this.loadIssueActivities(value)
      }
    },
    components: {
      ICol,
      labelEditorInput,
      labelEditorSelect,
      labelEditorVueEditor,
      VueEditor
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  @import './ProjectIssueStatus';

  .issue-detail {
    font-size: 14px;
    color: #b2b2b2;
  }

  .issue-title {
    padding: 10px 16px 10px 16px;
  }

  .issue-detail-body {

  }

  .issue-detail-summary {
    padding: 10px 16px 0px 16px;
  }

  .issue-detail-desc {
    padding: 16px;
  }

  .issue-detail-option {
    padding: 16px;
  }

  .issue-detail-attachment {
    padding: 16px;
  }

  .issue-detail-comments {
    padding: 16px;
    min-height:300px;
    color: #b2b2b2;
    background-color: #f8f9fa;
  }

  .issue-comments-input {
    position: fixed;
    bottom: 0px;
    height: 40px;
    width: 60%;
  }

  .issue-detail-id {
    display: inline-block;
    font-weight: 400;
    color: #666;
    font-size: 18px;
  }

  .issue-default-title {
    display: inline-block;
    font-weight: 400;
    color: #444;
    font-size: 18px;
  }

  .issue-detail-title {
    display: inline-block;
    font-weight: 400;
    color: #444;
    font-size: 18px;
    width: 60%;
  }

  .issue-detail-creation {
    font-size: 13px;
    color: #b2b2b2;
  }

  .issue-detail-creator {
    display: inline-block;
    padding: 0px 0px 0px 15px;
  }

  .issue-detail-createdate {
    display: inline-block;
    padding: 0px 0px 5px 5px;
  }

  .issue-detail-topic {
    font-size: 15px;
    font-weight: 400;
    padding: 0px 20px 10px 15px;
  }

  .issue-detail-topic-content {
    vertical-align: middle;
    color: #3b73af;
    padding: 5px 0px 0px 10px;
  }

  .issue-detail-topic-field-name {
    color: #b2b2b2;
  }
  .issue-detail-desc-title
  {
    margin-bottom:2px;
    color:#b2b2b2;
    padding:0px 5px 5px 0px;
    font-size: 14px;
  }

  .issue-detail-desc-content-veiw
  {
    outline:none;
    border:none;
    overflow:scroll;
    max-height:350px;
    min-height:80px;margin-bottom:2px;
    color:#b2b2b2;
    padding:5px 5px 10px 10px;
    margin-left:16px;
  }

  .issue-detail-field-content
  {
    padding-bottom:2px;
    color:#b2b2b2;
    padding:0px 5px 5px 20px;
    font-size: 14px;
  }
  .issue-detail-body a
  {
    color: #3b73af;
  }

  .attachment-item
  {
    padding: 5px 10px 5px 15px;
    font-size:14px;
    color:#3b73af;
  }


</style>
