<template>
  <div>
    <Card :dis-hover="true" style="width: 100%;margin-left: 5px;background-color: inherit">
      <Row>
        <i-col :span="4" style="width: 80px;padding-top: 15px;">
          <div style="display: inline-block" class="cursor-hand">
        <span @click="sendReport">
          <Avatar shape="square" size="large" style="height: 60px;width:60px;background-color: #fff;color:#777777">
        <Icon type="ios-send-outline" />
        发送</Avatar>
        </span>
          </div>
          <Divider type="vertical"  style="height:100px;"/>
        </i-col>
        <i-col :span="20">
          <div style="display:inline-block;">
            <Row style="padding: 5px;">
              <!--<i-col :span="6" style="width: 60px;">收件人：</i-col>-->
              <i-col style="min-width: 700px;">
                <span style="width: 60px;padding-right: 10px; display: inline-block">收件人:</span>
                <Select v-model="reportData.Recipients" filterable multiple>
                  <Option v-for="item in projectMembers" :value="item.PMMember" :key="item.id">{{ item.name }} ({{ item.email }})</Option>
                </Select></i-col>
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

         <table>
           <tr>
             <td style="width: 160px;">项目名称</td>
             <td style="padding: 0px;"><Input v-model="reportData.ProjectInfo.Project" placeholder="提测项目信息" style="width: 600px"/></td>
           </tr>
           <tr>
             <td>版本</td>
             <td style="padding: 0px;"><Input v-model="reportData.ProjectInfo.Version" placeholder="提测版本" style="width: 600px"/></td>
           </tr>
           <tr>
             <td>测试人员</td>
             <td style="padding: 0px;"><Input v-model="reportData.ProjectInfo.Tester" placeholder="测试人员，可多个" style="width: 600px"/></td>
           </tr>
           <tr>
             <td>开发人员</td>
             <td style="padding: 0px;"><Input v-model="reportData.ProjectInfo.Dev" placeholder="项目所有开发人员，前端，服务端，数据，客户端" style="width: 600px"/>
             </td>
           </tr>
           <tr>
             <td>PM</td>
             <td style="padding: 0px;"><Input v-model="reportData.ProjectInfo.PM" placeholder="产品，项目相关人员" style="width: 600px"/></td>
           </tr>
           <tr>
             <td>测试开始日期</td>
             <td style="padding: 0px;"><Input v-model="reportData.ProjectInfo.StartDate" placeholder="测试开始日期" style="width: 600px"/></td>
           </tr>
         </table>


         <Divider style="width: 760px;" orientation="center">检查点</Divider>
         <table>
           <tr>
             <th>检查点
               <span @click="addNewFeature"><Icon type="md-add-circle" :size="16" color="#32be77"
                                                  class="cursor-hand"/></span>
             </th>
             <th>未通过</th>
           </th>
           <tr v-for="feature in reportData.FeatureProgress.Feature" :key="feature.id">
             <td style="padding: 0px;"><Input v-model="feature.Content" placeholder="feature.Content" style="width: 600px" /></td>
             <td style="width: 160px;">
               <Checkbox v-model="feature.Passed1"></Checkbox>
               <span @click="removeFeature(feature.id)"><Icon type="md-close-circle" :size="16" color=""
                                                              class="cursor-hand"/></span>
             </td>
           </tr>
         </table>



         <Divider style="width: 760px;" orientation="center" >未通过情况描述</Divider>
         <div>
             <vue-editor v-model="reportData.BVTDetailResult" :editorToolbar="editorToolBar" style="width: 760px;" placeholder="BVT未通过用例详细情况"></vue-editor>
         </div>

         <Divider style="width: 760px;" orientation="center" >结论</Divider>
         <div>
           <vue-editor v-model="reportData.BVTVerdict" :editorToolbar="editorToolBar" style="width: 760px;" placeholder="BVT测试结论，是否可继续测试"></vue-editor>
         </div>
       </div>
    </div>
  </div>
</template>

<script>
  import ICol from '../../../../../node_modules/iview/src/components/grid/col.vue'
  import { VueEditor } from 'vue2-editor'
  import store from '../../../../store/index.js'
  import { mapGetters,mapMutations} from 'vuex'

  export default {
    components: {VueEditor,ICol},
    name: 'bvtReport',
    props: ['projectID','fortestingID'],
    data () {
      return {
        projectMembers: [],
        newReport: true,
        fortestingContent: [],
        defaultBTAttachments: [],
        editorToolBar: [
          ['bold', 'italic', 'underline'],
          [{'list': 'ordered'}, {'list': 'bullet'}],[{ 'color': [] }, { 'background': [] }],
        ],
        projectMembers: [],
        reportData: {}
      }
    },
    computed: {
      ...mapGetters(['appBodyHeight','userInfo']),
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
        console.log(this.reportData)
        this.$axios.post('/api/project/report/bvt',this.reportData).then(response => {
          this.$Message.success({
            content: 'BVT报告已经发送!',
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

      loadForTesting:  function () {
        this.$axios.get('/api/project/fortesting/'+this.fortestingID).then(response => {
          let fortesting = response.data.result
          if(this.newReport)
          {
            this.reportData.ProjectInfo.Version = fortesting.VersionName
            this.reportData.ProjectInfo.Project = fortesting.ProjectName
            this.reportData.id = this.fortestingID
            this.reportData.Topic = fortesting.ProjectName+'--'+fortesting.VersionName+'BVT通报--'+ new Date().toLocaleDateString()
            this.reportData.FeatureProgress.BugSummary = '见详情'
            this.reportData.FeatureProgress.Progress = '100%'
            for(let i=0; i<fortesting.FortestingFeature.length;i++)
            {
              let feature = {}
              feature['id'] = new Date().getTime()+ Math.random()
              feature['Content'] = fortesting.FortestingFeature[i]
              feature['Passed1'] = false
              feature['Passed2'] = false
              feature['Passed3'] = false
              this.reportData.FeatureProgress.Feature.push(feature)
            }
          }
          else
          {
            for(let i=0; i<this.reportData.FeatureProgress.Feature.length;i++)
            {
              this.reportData.FeatureProgress.Feature[i].id = new Date().getTime()+ Math.random()
            }

          }
        }, response => {

        })
      },

      addNewFeature: function () {
        let feature = {}
        feature['id'] = new Date().getTime()+Math.random()
        feature['Content'] = ''
        feature['Passed1'] = false
        feature['Passed2'] = false
        feature['Passed3'] = false
        this.reportData.FeatureProgress.Feature.push(feature)
      },

      handleSuccess (res, file, fileList) {
        file.url = res.result.url
        file.id = res.result.file_id
        let temp ={}
        temp['name']= file.name
        temp['url']= file.url
        this.reportData.BugTrendAttachments.push(temp)
      },

      handleRemove (file, fileList) {
        for(let i=0;i<this.reportData.BugTrendAttachments.length;i++)
        {
          if(this.reportData.BugTrendAttachments[i].url === file.url)
          {
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
        if(this.reportData.FortestingID === null)
        {
          this.newReport = true
          this.reportData.FortestingID = this.fortestingID
          this.reportData.ReportType =2
          this.reportData.ProjectInfo.StartDate = new Date().toLocaleDateString()
          this.reportData.Recipients.push(this.userInfo.id)
          this.reportData.ProjectInfo.Tester = this.userInfo.last_name+this.userInfo.first_name
        }
        else{
          this.newReport = false
        }
      },
      loadReport: function () {
        this.$axios.get('/api/project/fortesting/'+this.fortestingID+'/1').then(response => {
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
    watch: {
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  table, th, td
  {
    border: 1px solid lightgray;
    padding: 2px;
    padding-left: 5px;
    padding-right: 5px;
  }
</style>
