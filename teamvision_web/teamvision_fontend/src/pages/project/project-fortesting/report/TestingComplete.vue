<template>
  <div :style="'overflow:scroll;height:'+reportContainerHeight+'px'">
    <Card :dis-hover="true" style="width: 100%;margin-left: 5px;background-color: inherit">
      <Row>
        <i-col :span="4" style="width: 80px;padding-top: 15px;">
          <div style="display: inline-block" class="cursor-hand">
         <span @click="sendReport ">
              <Avatar shape="square" size="large" style="height: 60px;width:60px;background-color: #fff;color:#777777">
                <Icon type="ios-send-outline"/>
               发送</Avatar>
              </span>
          </div>
          <Divider type="vertical" style="height:100px;"/>
        </i-col>
        <i-col :span="20">
          <div style="display:inline-block;">
            <Row style="padding: 5px;">
              <!--<i-col :span="6" style="width: 60px;">收件人：</i-col>-->
              <i-col style="min-width: 700px;">
                <span style="width: 60px;padding-right: 10px; display: inline-block">收件人:</span>
                <Select v-model="reportData.Recipients" filterable multiple>
                  <Option v-for="item in projectMembers" :value="item.PMMember" :key="item.id">{{ item.name
                    }} ({{ item.email }})
                  </Option>
                </Select>
              </i-col>
            </Row>
            <Row style="padding: 5px;">
              <i-col style="min-width: 700px;">
                <span style="width: 60px;padding-right: 10px; display: inline-block">抄送:</span>
                <Input v-model="reportData.CCList" placeholder="输入邮箱，多人用逗号分隔" style="width: 100%"/>
              </i-col>
            </Row>
            <Row style="padding: 5px;">
              <i-col stype="min-width: 700px;">
                <span style="width: 60px;padding-right: 10px; display: inline-block">主题:</span>
                <Input v-model="reportData.Topic" placeholder="报告主题" style="width: 100%"/>
              </i-col>
            </Row>
          </div>
        </i-col>
      </Row>

    </Card>
    <div style="padding: 10px;padding-left: 100px;">
      <div>

        <Divider style="width: 760px;" orientation="center">重点提示</Divider>
        <div>
          <vue-editor v-model="reportData.Comments" :editorToolbar="editorToolBar" style="width: 760px;"
                      placeholder="报告开头内容，需要收件人重点关注的信息例如@张三"></vue-editor>
        </div>


        <Divider style="width: 760px;" orientation="center">上线通报</Divider>
        <table>
          <tr>
            <td><Input v-model="reportData.ReleaseNotification.Title" placeholder="【XXX项目】上线准备通报" style="width: 760px"/>
            </td>
          </tr>
          <tr>
            <td>
          <tr>
            <td style="width: 100px;">测试人员</td>
            <td><Input v-model="reportData.ReleaseNotification.Tester" placeholder="测试人员" style="width: 280px"/></td>
            <td style="width: 100px;">完成度</td>
            <td><Input v-model="reportData.ReleaseNotification.Progress" placeholder="完成度" style="width: 280px"/></td>
          </tr>
          </td>
          </tr>
          <tr>
            <td>
          <tr>
            <td style="width: 100px;">预计上线时间</td>
            <td><Input v-model="reportData.ReleaseNotification.ReleaseDate" placeholder="预计上线时间" style="width: 280px"/>
            </td>
            <td style="width: 100px;">上线项目</td>
            <td><Input v-model="reportData.ReleaseNotification.Project" placeholder="上线项目名称" style="width: 280px"/></td>
          </tr>
          </td>
          </tr>
          <tr>
            <td>
          <tr>
            <td style="width: 100px;">上线责任人</td>
            <td>
          <tr>
            <td style="width: 100px;">QA</td>
            <td><Input v-model="reportData.ReleaseNotification.QA" placeholder="QA本次上线负责人" style="width: 560px"/></td>
          </tr>
          <tr>
            <td style="width: 100px;">服务端</td>
            <td><Input v-model="reportData.ReleaseNotification.Service" placeholder="服务端本次上线开发负责人"
                       style="width: 560px"/></td>
          </tr>
          <tr>
            <td style="width: 100px;">前端</td>
            <td><Input v-model="reportData.ReleaseNotification.FE" placeholder="前端本次上线负责人" style="width: 560px"/></td>
          </tr>
          <tr>
            <td style="width: 100px;">客户端</td>
            <td><Input v-model="reportData.ReleaseNotification.Client" placeholder="上线项目名称" style="width: 560px"/></td>
          </tr>
          <tr>
            <td style="width: 100px;">数据</td>
            <td><Input v-model="reportData.ReleaseNotification.Data" placeholder="客户端本次上线负责人" style="width: 560px"/>
            </td>
          </tr>
          <tr>
            <td style="width: 100px;">PM</td>
            <td><Input v-model="reportData.ReleaseNotification.PM" placeholder="PM本次上线负责人" style="width: 560px"/></td>
          </tr>

          </td>
          </tr>
          </td>
          </tr>
        </table>


        <Divider style="width: 760px;" orientation="center">功能点</Divider>
        <table>
          <tr>
            <th>
            </th>
            <th>
              功能点测试进度
            </th>
          <tr>
            <td style="width: 100px;">
              完成度
            </td>
            <td style="padding: 0px;"><Input v-model="reportData.FeatureProgress.Progress" placeholder="测试整体进度"
                                             style="width: 660px"/>
            </td>
          </tr>
          <tr>
            <td style="width: 100px;">
              功能点
              <span @click="addNewFeature"><Icon type="md-add-circle" :size="16" color="#32be77"
                                                 class="cursor-hand"/></span>
            </td>
            <td>
          <tr v-for="feature in reportData.FeatureProgress.Feature" :key="feature.id">
            <td style="padding: 0px;"><Input v-model="feature.Content" placeholder="提测功能点" style="width: 560px"/>
            </td>
            <td style="width: 100px;">
              <Checkbox v-model="feature.Passed1">完成</Checkbox>
              <span @click="removeFeature(feature.id)"><Icon type="md-close-circle" :size="16" color=""
                                                             class="cursor-hand"/></span>
            </td>
          </tr>

          </td>
          </tr>

          <tr>
            <td style="width: 100px;">
              Bug情况
            </td>
            <td style="padding: 0px;"><Input v-model="reportData.FeatureProgress.BugSummary" placeholder="提测相关bug情况汇总描述"
                                             style="width: 660px"/>
            </td>
          </tr>
        </table>

        <Divider style="width: 760px;" orientation="center">Bug趋势图</Divider>
        <div style="width: 760px;">
          <div v-for="attachment in  reportData.BugTrendAttachments" style="padding-bottom: 10px;">
            <img :src="attachment.url" :key="attachment.url" style="width: 760px"/>
          </div>
          <Upload ref="upload" multiple type="drag" paste action="/api/project/fortesting/upload_files"
                  :on-success="handleSuccess"
                  :on-remove="handleRemove"
                  :format="['jpg','jpeg','png']"
                  :max-size="10240"
                  :default-file-list="reportData.BugTrendAttachments"
                  :on-format-error="handleFormatError"
                  :on-exceeded-size="handleMaxSize">
            <div style="padding: 20px 0">
              <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
              <p>点击，拖拽，粘贴上传图片</p>
            </div>
          </Upload>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
  import ICol from '../../../../../node_modules/iview/src/components/grid/col.vue'
  import { VueEditor } from 'vue2-editor'
  import store from '../../../../store/index.js'
  import { mapGetters, mapMutations } from 'vuex'

  export default {
    components: {VueEditor, ICol},
    name: 'testingCompleteReport',
    props: ['projectID', 'fortestingID'],
    data () {
      return {
        projectMembers: [],
        newReport: true,
        fortestingContent: [],
        defaultBTAttachments: [],
        editorToolBar: [
          ['bold', 'italic', 'underline'],
          [{'list': 'ordered'}, {'list': 'bullet'}], [{'color': []}, {'background': []}],
        ],
        reportData: {}
      }
    },
    computed: {
      ...mapGetters(['appBodyHeight', 'userInfo']),
      reportContainerHeight: function () {
        return this.appBodyHeight - 33
      },

    },
    methods: {

      loadProjectMembers: function () {
        this.$axios.get('/api/project/' + this.projectID + '/project_members').then(response => {
          this.projectMembers = response.data.result
        }, response => {

        })
      },

      sendReport: function () {
        this.$axios.post('/api/project/report/testcomplete', this.reportData).then(response => {
          this.$Message.success({
            content: '测试完成报告已经发送!',
            duration: 10,
            closable: true
          })
        }, response => {
          this.$Message.warning({
            content: '除重点提示，抄送字段，其他字段均需要填写！',
            duration: 10,
            closable: true
          })
        })
      },

      loadForTesting: function () {
        this.$axios.get('/api/project/fortesting/' + this.fortestingID).then(response => {
          let fortesting = response.data.result
          if (this.newReport) {
            this.reportData.id = this.fortestingID
            this.reportData.Topic = fortesting.ProjectName + '--' + fortesting.VersionName + '测试完成通报--' + new Date().toLocaleDateString()
            this.reportData.ReleaseNotification.Title = fortesting.ProjectName + '--' + fortesting.VersionName + '上线准备通报'
            this.reportData.ReleaseNotification.Project = fortesting.ProjectName + '--' + fortesting.VersionName
            for (let i = 0; i < fortesting.FortestingFeature.length; i++) {
              let feature = {}
              feature['id'] = new Date().getTime() + Math.random() * 10
              feature['Content'] = fortesting.FortestingFeature[i]
              feature['Passed1'] = false
              feature['Passed2'] = false
              feature['Passed3'] = false
              this.reportData.FeatureProgress.Feature.push(feature)
            }
          } else {
            for (let i = 0; i < this.reportData.FeatureProgress.Feature.length; i++) {
              this.reportData.FeatureProgress.Feature[i].id = new Date().getTime() + Math.random()
            }

          }
        }, response => {

        })
      },

      addNewFeature: function () {
        let feature = {}
        feature['id'] = new Date().getTime() + Math.random() * 10
        feature['Content'] = ''
        feature['Passed1'] = false
        feature['Passed2'] = false
        feature['Passed3'] = false
        this.reportData.FeatureProgress.Feature.push(feature)
      },

      handleSuccess (res, file, fileList) {
        file.url = res.result.url
        file.id = res.result.file_id
        let temp = {}
        temp['name'] = file.name
        temp['url'] = file.url
        this.reportData.BugTrendAttachments.push(temp)
      },

      handleRemove (file, fileList) {
        for (let i = 0; i < this.reportData.BugTrendAttachments.length; i++) {
          if (this.reportData.BugTrendAttachments[i].url === file.url) {
            this.reportData.BugTrendAttachments.pop(this.reportData.BugTrendAttachments[i])
          }
        }
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

      removeFeature: function (key) {
        if (key !== 0) {
          for (let i = 0; i < this.reportData.FeatureProgress.Feature.length; i++) {
            let temp = this.reportData.FeatureProgress.Feature[i]
            if (temp.id === key) {
              this.reportData.FeatureProgress.Feature.splice(i,1)
              break
            }
          }
        }
      },
      initReport: function () {
        if (this.reportData.FortestingID === null) {
          this.newReport = true
          this.reportData.FortestingID = this.fortestingID
          this.reportData.ReportType = 3
          this.reportData.ReleaseNotification.ReleaseDate = new Date().toLocaleDateString()
          this.reportData.ReleaseNotification.Tester = this.userInfo.last_name + this.userInfo.first_name
          this.reportData.ReleaseNotification.QA = this.reportData.ReleaseNotification.Tester
          this.reportData.Recipients.push(this.userInfo.id)
        }
        else {
          this.newReport = false
        }
      },
      loadReport: function () {
        this.$axios.get('/api/project/fortesting/' + this.fortestingID + '/3').then(response => {
          this.reportData = response.data.result
          this.loadForTesting()
          this.initReport()

        }, response => {

        })

      }
    },
    created: function () {
      this.loadProjectMembers()
      this.loadReport()
    },
    watch: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  table, th, td {
    border: 1px solid lightgray;
    text-align: center;
    /*padding: 2px;*/
    /*padding-left: 5px;*/
    /*padding-right: 5px;*/
  }
</style>
