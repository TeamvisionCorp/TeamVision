<template>
  <Modal :value="dialogShow" title="添加新问题" :mask-closable="false" :width="600" @on-cancel="cancel" :styles="{bottom:'20px',top: '50px'}">
    <div :style="'height:' + containerHeight + 'px;overflow-y: scroll;overflow-x: hidden'">
      <Form ref="createIssue" :model="formItem" :label-width="80" :rules="ruleCustom">
        <FormItem label="项目" prop="Project">
          <Cascader v-model="formItem.Project" :data="projectVersions" @on-change="onProjectChange"
                    :filterable="true"></Cascader>
        </FormItem>
        <FormItem label="标题" prop="Title">
          <Input v-model="formItem.Title" placeholder="问题概述"/>
        </FormItem>
        <FormItem label="经办人" prop="Processor">
          <Select v-model="formItem.Processor" :filterable="true" placeholder="默认为创建者">
            <Option v-for="member in projectMembers" :key="member.PMMember" :value="member.PMMember">{{ member.name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="团队" prop="Team">
          <Select v-model="formItem.Team" :filterable="true" placeholder="选择项目角色">
            <Option v-for="team in projectTeams" :key="team.id" :value="team.id">{{ team.Name }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="描述" prop="Desc">
            <vue-editor v-model="formItem.Desc" :editorToolbar="editorToolBar"  placeholder="问题描述"></vue-editor>
        </FormItem>
        <Row>
          <i-col :span="12">
            <FormItem label="模块" prop="Module">
              <Select v-model="formItem.Module" :filterable="true" placeholder="问题所属模块">
                <Option v-for="module in projectModules" :key="module.id" :value="module.id">{{ module.Name }}
                </Option>
              </Select>
            </FormItem>
          </i-col>
          <i-col :span="12">
            <FormItem label="分类" prop="IssueCategory">
              <Select v-model="formItem.IssueCategory" :filterable="true" placeholder="请选择分类">
                <Option v-for="category in issueCategories" :key="category.Value" :value="category.Value">{{ category.Name }}
                </Option>
              </Select>
            </FormItem>
          </i-col>
        </Row>
        <Row>
          <i-col :span="12">
            <FormItem label="严重性" prop="Severity">
              <Select v-model="formItem.Severity" :filterable="true" placeholder="默认为创建者">
                <Option v-for="severity in issueSeverity" :key="severity.Value" :value="severity.Value">{{ severity.Name }}
                </Option>
              </Select>
            </FormItem>
          </i-col>
          <i-col :span="12">
            <FormItem label="阶段" prop="ProjectPhase">
              <Select v-model="formItem.ProjectPhase" :filterable="true" placeholder="默认为创建者">
                <Option v-for="phrase in issueProjectPhrase" :key="phrase.Value" :value="phrase.Value">{{ phrase.Name }}
                </Option>
              </Select>
            </FormItem>
          </i-col>
        </Row>
        <Row>
          <i-col :span="12">
            <FormItem label="系统" prop="DeviceOS">
              <Select v-model="formItem.DeviceOS" :filterable="true" placeholder="默认为创建者">
                <Option v-for="os in DeviceOS" :key="os.Value" :value="os.Value">{{ os.Name }}
                </Option>
              </Select>
            </FormItem>
          </i-col>
          <i-col :span="12">
            <FormItem label="优先级" prop="Priority">
              <Select v-model="formItem.Priority" :filterable="true" placeholder="默认为创建者">
                <Option v-for="priority in IssuePriority" :key="priority.Value" :value="priority.Value">{{ priority.Name }}
                </Option>
              </Select>
            </FormItem>
          </i-col>
        </Row>
        <FormItem>
          <Upload ref="upload" multiple type="drag" paste action="/api/project/issue/attachments"
                  :on-success="handleSuccess"
                  :on-remove="handleRemove"
                  :format="[]"
                  :max-size="10240"
                  :default-file-list="formItem.defaultList"
                  :on-format-error="handleFormatError"
                  :on-exceeded-size="handleMaxSize">
            <div style="padding: 20px 0">
              <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
              <p>点击，拖拽，粘贴上传附件</p>
            </div>
          </Upload>
        </FormItem>
      </Form>
    </div>
    <div slot="footer">
      <Button v-if="createDialogShow" type="success" style="width: 80px; height:30px;" shape="circle"
              @click="ok('createIssue')">添加
      </Button>
    </div>
  </Modal>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
import { VueEditor } from 'vue2-editor'
import { initProjectVersions, issueValidateRules } from './ProjectIssueCreateDialog'
import FormItem from '../../../../node_modules/iview/src/components/form/form-item.vue'

export default {
  name: 'ProjectIssueCreateDialog',
  props: {
    projectID: {
      type: [Number,String],
      default: 0
    },
    versionID: {
      type: [Number,String],
      default: 0
    }
  },

  data () {
    return {
      sourceProject: [],
      projectVersions: [],
      projectTeams: [],
      projectModules: [],
//      projectMembers: [],
      issueStatus: [],
      issueSeverity: [],
      issueResolvedResult: [],
      issueProjectPhrase: [],
      issueCategories: [],
      DeviceOS: [],
      IssuePriority: [],
      editorToolBar: [
        ['bold', 'italic', 'underline'],
        [{'list': 'ordered'}, {'list': 'bullet'}],[{ 'color': [] }, { 'background': [] }],
      ],
      formItem: {
        Title: '',
        Team: 0,
        Processor: 0,
        Severity: 0,
        Module: 0,
        Desc: '<p>步骤:</p></br><p>实际结果:</p></br><p>期望结果:</p>',
        Project: [],
        ProjectPhase: 0,
        IssueCategory: 0,
        DeviceOS: 0,
        Priority: 0,
        uploadList: [],
        defaultList: []
      },
      ruleCustom: {
        ...issueValidateRules
      }
    }

  },
  computed: {
    ...mapGetters('projectglobal', ['createDialogShow', 'viewDialogShow', 'projectVersion']),
    ...mapGetters(['appBodyHeight']),
    containerHeight: function () {
      return this.appBodyHeight-100
    },

    project: function() {
      return parseInt(this.projectID)
    },

    projectVersion: function() {

      return parseInt(this.versionID)

    },

    dialogShow: function () {
      return (this.createDialogShow || this.viewDialogShow)
    },

      projectMembers: function () {
        let project = this.formItem.Project[0]
        let result = []
        for (let i = 0; i < this.sourceProject.length; i++) {
          if (this.sourceProject[i].id === project) {
            result = this.sourceProject[i].Members
          }
        }
        return result
      }
    },
  methods: {
        ...mapMutations('projectglobal', ['setCreateDialogShow', 'setViewDialogShow', 'setTaskChange']),
        ...mapMutations('issue', ['setIssueChange']),

        ok (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {
              if (this.createDialogShow) {
                this.$axios.post('/api/project/' + this.formItem.Project[0] + '/version/' + this.formItem.Project[1] + '/issues', this.formItem).then(response => {
                  this.setIssueChange(true)
                }, response => {

                })
              }
              this.setCreateDialogShow(false)
            }
          })
        },
        cancel () {
          this.setCreateDialogShow(false)
        },

      handleSuccess (res, file, fileList) {
        file.url = res.result.url
        file.id = res.result.file_id
        this.formItem.uploadList.push(file.id)
      },

      handleRemove (file, fileList) {
        this.uploadList = fileList
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

      onProjectChange (value, selectedData) {
        let project = value[0]
        for (let i = 0; i < this.sourceProject.length; i++) {
          if (this.sourceProject[i].id === project) {
            this.projectMember = this.sourceProject[i].Members
            this.loadIssueProjectModules(project)
          }
        }
      },

      loadMyTeams: function () {
        this.$axios.get('/api/common/teams/my').then(response => {
          this.projectTeams = response.data.result
        }, response => {
        })
      },

      loadIssueStatus: function () {
        this.$axios.get('/api/project/issue/status').then(response => {
          this.issueStatus = response.data.result
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
        this.IssuePriority = response.data.result
      }, response => {
      })
    },

    loadIssueOS: function () {
      this.$axios.get('/api/project/issue/os').then(response => {
        this.DeviceOS = response.data.result
      }, response => {
      })
    },

      loadMyProject: function () {
        this.$axios.get('/api/project/list?extinfo=1&home=1').then(response => {
          let tempData = response.data.result
          this.sourceProject = tempData
          this.projectVersions = initProjectVersions(tempData)
        }, response => {
        })
      }

    },
  created () {
    this.loadMyProject()
    this.loadIssueSeverity()
    this.loadMyTeams()
    this.loadIssueProjectPriority()
    this.loadIssueOS()
    this.loadIssueProjectPhrase()
    this.loadIssueCategories()
    this.onProjectChange([].push(this.project))
    this.formItem.Project.push(this.project)
    this.formItem.Project.push(this.projectVersion)
    this.loadIssueProjectModules(this.project)
    },
  mounted () {
  },
  watch: {
    },
  components: {
    VueEditor,
    FormItem
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
