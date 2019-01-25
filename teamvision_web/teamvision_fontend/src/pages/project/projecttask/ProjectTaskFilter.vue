<template>
  <div>
    <Card :shadow="false" :padding="0" :bordered="false" dis-hover>

      <Row class="filter-block">
        <div class="filter-block-body">
          <Row>
            <Input  @on-search="onSearchTask" search placeholder="输入任务标题，回车搜索" />
          </Row>
        </div>
      </Row>

      <Row class="filter-block">
        <div class="filter-block-title">
          <p><i class="fa fa-eye"></i> 状态</p>
        </div>
        <div class="filter-block-body">
          <Row>
            <CheckboxGroup v-model="filterPanel.status" @on-change="onStatusChange">
              <i-col :lg="8" :sm="12">
                <Checkbox label="0" >
                       待处理
                </Checkbox>
              </i-col>
              <i-col :lg="8" :sm="12">
                <Checkbox label="1">
                  处理中
                </Checkbox>
              </i-col>
              <i-col :lg="8" :sm="12">
                <Checkbox label="2">
                  已完成
                </Checkbox>
              </i-col>

              <i-col :lg="8" :sm="12">
                <Checkbox label="3" >
                  暂停
                </Checkbox>
              </i-col>
            </CheckboxGroup>
          </Row>
        </div>
      </Row>

      <Row class="filter-block">
        <div class="filter-block-title">
          <p><i class="fa fa-hand-o-right fa-fw"></i> 执行人</p>
        </div>
        <div class="filter-block-body">
          <Select v-model="filterPanel.owners" filterable multiple @on-change="onOwnerChange">
            <Option v-for="item in projectMembers" :value="item.PMMember" :key="item.id">{{ item.name }}</Option>
          </Select>
        </div>
      </Row>

    </Card>
    <Divider orientation="left">统计</Divider>
    <Card :shadow="false" :padding="0" :bordered="false" dis-hover>
      <Row class="filter-block">
        <div class="filter-block-body">
          <Row>
              <i-col :lg="8" :sm="8" style="padding: 5px;">
                <Card dis-hover style="padding: 5px 5px 5px 5px;height: 70px;" :padding="0" >
                    <div style="font-size: 10px;">今日完成</div>
                    <div style="width: inherit;text-align: center;">{{ taskSummaryCount.today_finished_count }}</div>
                </Card>
              </i-col>
              <i-col :lg="8" :sm="8" style="padding: 5px;">
                <Card dis-hover style="padding: 5px 5px 5px 5px;height: 70px;" :padding="0">
                  <div style="font-size: 10px;">延期任务:</div>
                  <div style="width: inherit;text-align: center;">{{ taskSummaryCount.delayed_count }}</div>
                </Card>
              </i-col>
             <i-col :lg="8" :sm="8" style="padding: 5px;">
              <Card dis-hover style="padding: 5px 5px 5px 5px;height: 70px;" :padding="0">
                <div style="font-size: 10px;">延期完成</div>
                <div style="width: inherit;text-align: center;">{{ taskSummaryCount.delay_finished_count }}</div>
              </Card>
            </i-col>
          </Row>
        </div>
      </Row>
    </Card>
    <Card :shadow="false" :padding="0" :bordered="false" dis-hover>
      <div class="x-bar">
        <div :id="id"
             :option="pieChartOption"></div>
      </div>
    </Card>
  </div>
</template>

<script>
  import { mapGetters, mapMutations} from 'vuex'
  import HighCharts from 'highcharts'

  export default {
    name: 'projectTaskFilter',
    props: {
      projectID: {
        type: [Number,String]
      }
    },
    data () {
      return {
        projectMembers: [],
        filterPanel: {
          status: [],
          owners: [],
          keyWords: ''
        },
        id: 'taskStatusSummary',
        pieChartOption: {
          chart: {
            type: 'pie',
          },
          title: {
            text: '任务状态分布'
          },
          plotOptions: {
            pie: {
              allowPointSelect: true,
              cursor: 'pointer',
              dataLabels: {
                enabled: false
              },
              showInLegend: true
            }
          },
          tooltip: {
            headerFormat: '{series.name}<br>',
            pointFormat: '{point.name}: <b>{point.percentage:.1f}%</b>'
          },
          series: [{
            name: '任务占比',
            data: [
            ]
          }]

        },

        taskSummaryCount: {}

      }
    },
    computed: {
      ...mapGetters('task', ['taskChange','taskFilters']),
      ...mapGetters('projectglobal', ['projectVersion','rightSidePanelShow']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight-26
      },
      project: function () {
        let result = 0
        if( this.projectID )
        {
           result = this.projectID
        }
        return result
      }

    },
    methods:
      {
        ...mapMutations('task', ['setTaskChange', 'setTaskFilterStatus','setTaskFilterOwners','setTaskFilterKeyword']),
        ...mapMutations('projectglobal', ['setViewDialogShow']),

        getProjectMembers (project){
          this.$axios.get('/api/project/' + project + '/project_members').then(response => {
            this.projectMembers = response.data.result
          }, response => {
          })
        },

        onSearchTask (keyword) {
          this.setTaskFilterKeyword(keyword)
        },

        onStatusChange (value) {
          this.setTaskFilterStatus(value)
        },

        onOwnerChange (value) {
          this.setTaskFilterOwners(value)
        },

        setTaskStatusPie (projectID,versionID) {
          this.$axios.get('/api/project/' + projectID + '/version/' + versionID + '/statistics/task_status_pie').then(response => {
            this.pieChartOption.title.text = response.data.result.chart_title
            this.pieChartOption.series[0].data = response.data.result.series_data
            HighCharts.chart(this.id,this.pieChartOption)
          }, response => {
          })
        },

        setTaskSummaryCount (projectID,versionID) {
          this.$axios.get('/api/project/' + projectID + '/version/' + versionID + '/statistics/task_summary_count').then(response => {
            this.taskSummaryCount = response.data.result
          }, response => {
          })
        }

      },
    created: function () {
      this.getProjectMembers(this.project)
    },
    mounted: function () {
    },
    watch: {
      projectID: function (value) {
        this.getProjectMembers(value)
      },

      rightSidePanelShow: function (value) {
        if(value)
        {
           this.setTaskStatusPie(this.projectID,this.projectVersion)
           this.setTaskSummaryCount(this.projectID,this.projectVersion)
        }
      }
    },

    components: {
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .filter-block
  {
    margin-top: 15px;
    padding-left: 15px;
  }

  .filter-block-title
  {
    padding: 0px;
  }

  .filter-block-body
  {
    padding: 10px;
  }
</style>
