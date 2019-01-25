<template>
  <div class="home-summary">
    <Row :gutter="16">
      <Col :lg="18" :md="24" :sm="24" :xs="24" :style="'height:'+summaryHeight+'px'+'; overflow-y:scroll;'">
      <div >
        <Card  :padding="0" dis-hover>
          <div class="home-summary-card-title">
            待处理事项:
          </div>
          <Row type="flex" justify="space-between">
            <Col span="8" style="padding: 20px;">
               <Card :padding="20" style="height: 100px;" dis-hover>
                 <div class="summary-number-title">问题:</div>
                 <div class="summary-number-content">
                   <a href="/home/my/issue" style="color: inherit;">{{ toDoSummary.issueCount }}</a>
                 </div>
               </Card>
            </Col>
            <Col span="8"  style="padding: 20px" >
             <Card :padding="20" style="height: 100px;" dis-hover>
                 <div class="summary-number-title">提测:</div>
                 <div class="summary-number-content">
                   <a href="/home/my/fortesting" style="color: inherit;">
                     {{ toDoSummary.fortestingCount }}
                   </a>
                 </div>
             </Card>
            </Col>
            <Col span="8"  style="padding: 20px">
             <Card :padding="20" style="height: 100px;" dis-hover>

                 <div class="summary-number-title">任务:</div>
                 <div class="summary-number-content">
                   <a href="/home/my/task" style="color: inherit;">{{ toDoSummary.taskCount }}</a>
                 </div>
             </Card>
            </Col>
          </Row>
        </Card>
        <Card  :padding="0" style="margin-top: 20px;" dis-hover>
          <div class="home-summary-card-title">
            活跃项目:
          </div>
          <Row :gutter="16">
            <Col :lg="5" :md="6" :sm="8" :xs="12" v-for="project in activeProject" :key="project.id">
            <Card     style="width:230px;height:180px;float:left;margin:20px;" :bordered="false">
              <div style="text-align:center;height:110px;">
                <a :href="'/project/'+  project.id +'/issue/all'">
                  <img :src="''+project.PBAvatar" style="width:80%;height:80px;">
                </a>
              </div>
              <div style="padding-top: 10px;color:#333;text-align: center">{{ project.PBTitle }}</div>
            </Card>
            </Col>
          </Row>
        </Card>
      </div>
      </Col>
      <Col :lg="6" :md="0" :sm="0" :xs="0">
      <div >
        <Card  :padding="0" dis-hover>
          <div class="home-summary-card-title">
            动态:
          </div>
            <Timeline style="padding:20px; text-align: left;">
              <Scroll :on-reach-bottom="handleReachBottom" :height="activityHiehgt">
              <TimelineItem color="green" v-for="item in activity.data" :key="item.id">

                <div style="word-break: break-all;white-space: normal;" >
                  <span style="margin-right: 10px;">{{ item.ActionTimeStr }}</span>
                  <span style="margin-right: 10px;"><Avatar size="small" style="background-color:#388E8E">{{ item.UserName }}</Avatar></span>
                  <span style="margin-right: 10px;">{{ item.ChangeMessage }}</span>
                  <span>
                    {{ item.ObjectRepr }}
                  </span>

                </div>

              </TimelineItem>
                </Scroll>
            </Timeline>
        </Card>
      </div>
      </Col>
    </Row>
  </div>

</template>

<script>
  import store from '../../store/index.js'
  import { mapGetters,mapMutations} from 'vuex'
  import { getCookie } from '../../util/cookie'
  export default {
    name: 'HomeSummary',
    data () {
      return {
        toDoSummary: {
          taskCount: 0,
          issueCount: 0,
          fortestingCount: 0,
        },
        activeProject: [],
        activity: {
          next: '',
          data: [],
          count: 0
        }
      }
    },
    computed: {
      ...mapGetters(['appBodyHeight']),
      summaryHeight: function () {
        return  this.appBodyHeight - 33
      },
      activityHiehgt: function () {
        console.log(getCookie('sessionid'))
        return this.appBodyHeight - 110
      }
    },
    methods: {
      handleReachBottom: function () {
        this.$axios.get(this.activity.next).then(response => {
          this.activity.count = response.data.result.count
          this.activity.next = response.data.result.next
          this.activity.data.push(...response.data.result.results)
        }, response => {
        })
      },
      loadToDoSummary: function () {
        this.$axios.get('/api/home/todo/summary').then(response => {
          this.toDoSummary.taskCount=response.data.result.task_count
          this.toDoSummary.issueCount=response.data.result.issue_count
          this.toDoSummary.fortestingCount=response.data.result.fortesting_count
        }, response => {
        })
      },

      loadMyProjectList: function () {
        this.$axios.get('/api/project/list?latest=1&my=1').then(response => {
          this.activeProject = response.data.result
        }, response => {
        })
      },
      loadActivity: function () {
        this.$axios.get('/api/home/activity/list').then(response => {
          this.activity.count = response.data.result.count
          this.activity.next = response.data.result.next
          this.activity.data = response.data.result.results
        }, response => {
        })
      }
    },
    created: function () {
      this.loadToDoSummary()
      this.loadMyProjectList()
      this.loadActivity()
    },
    componets: {
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .home-summary{
    padding-left:20px;
    padding-right:20px;

  }
  .home-summary-card-title
  {
    height:41px;
    text-align: left;
    padding-left: 20px;
    padding-top:10px;
    background-color: #f5f7f9;
  }
  .summary-number-title{
    text-align: left;
    margin-left: -10px;
    margin-top: -18px;
    font-size: 18px;
  }

  .summary-number-content{
    text-align: center;
    font-size: 30px;
  }

  .content{
    padding-left: 5px;
  }

</style>
