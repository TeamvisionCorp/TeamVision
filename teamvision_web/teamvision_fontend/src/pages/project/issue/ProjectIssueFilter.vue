<template>
  <div>
    <Card :shadow="false" :padding="0" :bordered="false" dis-hover
          style="border-left: 1px solid #e4e5e7;border-top: 1px solid #e4e5e7;">
      <div style="height: 40px;border-bottom: 1px solid #e4e5e7;padding:10px;padding-top: 10px;">
             <span>
               <!--<Dropdown trigger="click" style="margin-left: 20px">-->
                <!--<span class="cursor-hand" style="font-size: 12px;">-->
                 <!--筛选-->
                  <!--<Icon type="ios-arrow-down"></Icon>-->
                 <!--</span>-->
                  <!--<DropdownMenu slot="list">-->
                  <!--<DropdownItem>驴打滚</DropdownItem>-->
                  <!--<DropdownItem>炸酱面</DropdownItem>-->
                  <!--<DropdownItem>豆汁儿</DropdownItem>-->
                  <!--<DropdownItem>冰糖葫芦</DropdownItem>-->
                  <!--<DropdownItem>北京烤鸭</DropdownItem>-->
                  <!--</DropdownMenu>-->
               <!--</Dropdown>-->
                  </span>
        <span class="pull-right">
               <!--<ButtonGroup size="small">-->
        <!--<Button icon="ios-trash ">-->
            <!--清除-->
        <!--</Button>-->
    <!--</ButtonGroup>-->
             </span>
      </div>
      <div :style="'overflow-y:auto;height:'+containerHeight+'px'">
        <Row v-if="$route.name !== 'homeIssue'" class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-file fw"></i> 项目</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.projects" filterable multiple @on-change="onProjectChange">
              <Option v-for="item in myProjectList" :value="item.id" :key="item.id">{{ item.PBTitle }}</Option>
            </Select>
          </div>
        </Row>

        <Row v-if="$route.name !== 'homeIssue'" class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-road fa-fw"></i> 版本</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.versions" filterable multiple :disabled="projectVersions.disable" @on-change="onFiltersChange">
              <Option v-for="item in projectVersions.values" :value="item.id" :key="item.id">{{ item.VVersion }}
              </Option>
            </Select>
          </div>
        </Row>


        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-eye"></i> 状态</p>
          </div>
          <div class="filter-block-body">
            <Row>
              <CheckboxGroup v-model="filterPanel.status" @on-change="onFiltersChange">
                <i-col v-for="item in issueStatus" :key="item.id" :lg="8" :sm="12">
                  <Checkbox :label="item.Value">
                    <i :class="'fa '+item.Label+' '+item.LabelStyle"></i>
                    <span>{{ item.Name }}</span>
                  </Checkbox>
                </i-col>
              </CheckboxGroup>
            </Row>
          </div>
        </Row>

        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-shield fa-fw"></i> 严重性</p>
          </div>
          <div class="filter-block-body">
            <Row>
              <CheckboxGroup v-model="filterPanel.severity" @on-change="onFiltersChange">
                <i-col v-for="item in issueSeverity" :lg="8" :sm="12" :key="item.id">
                  <Checkbox :label="item.Value">
                    <i :class="'fa '+item.Label+' '+item.LabelStyle"></i>
                    <span>{{ item.Name }}</span>
                  </Checkbox>
                </i-col>
              </CheckboxGroup>
            </Row>
          </div>
        </Row>

        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-group fa-fw"></i> 优先级</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.issuePriority" filterable multiple @on-change="onFiltersChange">
              <Option v-for="item in IssuePriority" :value="item.Value" :key="item.Value">{{ item.Name }}</Option>
            </Select>
          </div>
        </Row>

        <Row v-if="$route.name !== 'homeIssue'" class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-group fa-fw"></i> 团队</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.teams" filterable multiple @on-change="onFiltersChange">
              <Option v-for="item in projectTeams" :value="item.id" :key="item.id">{{ item.Name }}</Option>
            </Select>
          </div>
        </Row>

        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-hand-o-right fa-fw"></i> 经办人</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.processors" filterable multiple :disabled="projectMembers.disable" @on-change="onFiltersChange">
              <Option v-for="item in projectMembers.values" :value="item.id" :key="item.id">{{ item.name }}</Option>
            </Select>
          </div>
        </Row>
        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-user fa-fw"></i> 报告人</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.reportors" filterable multiple :disabled="projectMembers.disable" @on-change="onFiltersChange">
              <Option v-for="item in projectMembers.values" :value="item.id" :key="item.id">{{ item.name }}</Option>
            </Select>
          </div>
        </Row>

        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-calendar-o fa-fw"></i> 创建时间</p>
          </div>
          <div class="filter-block-body">
            <DatePicker v-model="filterPanel.createTimeRange" format="yyyy-MM-dd"  type="daterange" show-week-numbers placement="bottom-end" transfer placeholder="创建时间范围" @on-change="onFiltersChange" style="width: 100%;"></DatePicker>
          </div>
        </Row>

        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-group fa-fw"></i> 项目阶段</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.projectPhrases" filterable multiple @on-change="onFiltersChange">
              <Option v-for="item in issueProjectPhrase" :value="item.Value" :key="item.Value">{{ item.Name }}</Option>
            </Select>
          </div>
        </Row>

        <Row class="filter-block">
          <div class="filter-block-title">
            <p><i class="fa fa-group fa-fw"></i> 问题分类</p>
          </div>
          <div class="filter-block-body">
            <Select v-model="filterPanel.issueCategories" filterable multiple @on-change="onFiltersChange">
              <Option v-for="item in issueCategories" :value="item.Value" :key="item.Value">{{ item.Name }}</Option>
            </Select>
          </div>
        </Row>


        <Row class="filter-block" style="min-height: 150px;">
          <div class="filter-block-title">
            <p><i class="fa fa-braille fa-fw"></i> 解决结果</p>
          </div>
          <div class="filter-block-body">
            <Row>
              <CheckboxGroup v-model="filterPanel.resolveResult" @on-change="onFiltersChange">
                <i-col v-for="item in issueResolvedResult" :lg="8" :sm="12" :key="item.id">
                  <Checkbox :label="item.Value">
                    <i :class="'fa '+item.Label+' '+item.LabelStyle"></i>
                    <span>{{ item.Name }}</span>
                  </Checkbox>
                </i-col>
              </CheckboxGroup>
            </Row>

          </div>
        </Row>

      </div>
    </Card>
  </div>
</template>

<script>
  import {mapGetters, mapMutations} from 'vuex'

  export default {
    name: 'projectIssueFilter',
    props: {
      projectID: {
        type: [Number, String]
      }
    },
    data() {
      return {
        columnItemHeight: 200,
        myProjectList: [],
        projectVersions: {
          disable: false,
          values: []
        },
        projectMembers: {
          disable: false,
          values: []
        },
        projectTeams: [],
        issueStatus: [],
        issueSeverity: [],
        issueResolvedResult: [],
        issueProjectPhrase: [],
        issueCategories: [],
        IssuePriority: [],

        filterPanel: {
          projects: [],
          versions: [],
          teams: [],
          status: [],
          processors: [],
          reportors: [],
          createTimeRange: '',
          resolveResult: [],
          severity: [],
          projectPhrases: [],
          issueCategories: [],
          issuePriority: []

        }
      }
    },
    computed: {
      ...mapGetters('task', ['taskChange']),
      ...mapGetters('projectglobal', ['projectVersion']),
      ...mapGetters(['appBodyHeight', 'userInfo']),
      containerHeight: function () {
        return this.appBodyHeight - 36
      },
      project: function () {
        let result = 0
        if (this.projectID) {
          result = this.projectID
        }
        return result
      }

    },
    methods:
      {
        ...mapMutations('issue', ['setIssueFilters']),
        ...mapMutations('projectglobal', ['setViewDialogShow']),


        onFiltersChange: function (value) {
          console.log(value)
          this.setFilters(value)
        },

        setFilters: function (value) {
          let filters = ''
          // 生成项目ID过滤
          if (this.filterPanel.projects.length>0) {

            filters = filters + 'Project__in='+ this.filterPanel.projects + ',0&'
          }

          // 生成版本过滤
          if (this.filterPanel.versions.length>0) {
            filters = filters + 'Version__in=' + this.filterPanel.versions + ',0&'
          }

          // 生成状态过滤
          if (this.filterPanel.status.length>0) {
            filters = filters + 'Status__in=' + this.filterPanel.status + ',0&'
          }
          // 生成严重性过滤
          if (this.filterPanel.severity.length>0) {
            filters = filters + 'Severity__in=' + this.filterPanel.severity + ',0&'
          }

          // 生成优先级过滤
          if (this.filterPanel.issuePriority.length>0) {
            filters = filters + 'Priority__in=' + this.filterPanel.issuePriority + ',0&'
          }

          // 生成团队过滤
          if (this.filterPanel.teams.length>0) {
            filters = filters + 'Team__in=' + this.filterPanel.teams + ',0&'
          }

          // 生成经办人过滤
          if (this.filterPanel.processors.length>0) {
            filters = filters + 'Processor__in=' + this.filterPanel.processors + ',0&'
          }

          // 生成报告人过滤
          if (this.filterPanel.reportors.length>0) {
            filters = filters + 'Creator__in=' + this.filterPanel.reportors + ',0&'
          }

          // 生成创建时间过滤
          if (this.filterPanel.createTimeRange.length > 1) {
            console.log(this.filterPanel.createTimeRange)
            if ( this.filterPanel.createTimeRange[0] !== '') {
              filters = filters + 'CreationTime__range=' + value + '&'
            }

          }
          // 生成项目阶段过滤
          if (this.filterPanel.projectPhrases.length>0) {
            filters = filters + 'ProjectPhase__in=' + this.filterPanel.projectPhrases + ',0&'
          }
          // 生成问题分类过滤
          if (this.filterPanel.issueCategories.length>0) {
            filters = filters + 'IssueCategory__in=' + this.filterPanel.issueCategories + ',0&'
          }
          // 生成解决结果过滤
          if (this.filterPanel.resolveResult.length>0) {
            filters = filters + 'Solution__in=' + this.filterPanel.resolveResult + ',0&'
          }
          console.log(filters)
          console.log(this.filterPanel)
          this.setIssueFilters(filters)
        },

        loadMyProject: function () {
          this.$axios.get('/api/project/list?extinfo=1&my=1').then(response => {
            this.myProjectList = response.data.result
          }, response => {
          })
        },

        initFilterPanel: function () {
          this.loadMyProject()
          this.filterPanel.projects = []
          this.filterPanel.processors = []
          if (parseInt(this.project)!==0) {
            this.filterPanel.projects.push(parseInt(this.project))
          }

          if (this.$route.name === 'homeIssue') {
            this.filterPanel.processors.push(parseInt(this.userInfo.id))
            this.filterPanel.status.push(2)
            this.filterPanel.status.push(4)
            let filters = 'Status__in=2,4&Processor__in=' + this.userInfo.id
            this.setIssueFilters(filters)
            let currentUser = {}
            currentUser['id'] = parseInt(this.userInfo.id)
            currentUser['name'] = this.userInfo.last_name + this.userInfo.first_name
            this.projectMembers.values.push(currentUser)
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

        loadIssueReslovedResult: function () {
          this.$axios.get('/api/project/issue/resolve_results').then(response => {
            this.issueResolvedResult = response.data.result
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

        loadIssueProjectPriority: function () {
          this.$axios.get('/api/project/issue/priority').then(response => {
            this.IssuePriority = response.data.result
          }, response => {
          })
        },

        onProjectChange: function (value) {
          this.setFilters()
          if (value.length > 1 || value.length === 0) {
            this.projectVersions.disable = true
            this.projectMembers.disable = true
          } else {
            this.projectVersions.disable = false
            this.projectMembers.disable = false
            for (let i = 0; i < this.myProjectList.length; i++) {
              if (this.myProjectList[i].id === parseInt(value[0])) {
                this.projectVersions.values = this.myProjectList[i].Versions
                this.projectMembers.values = this.myProjectList[i].Members
              }
            }
          }
        }
      },
    created: function () {
      this.initFilterPanel()
      this.loadIssueStatus()
      this.loadIssueSeverity()
      this.loadMyTeams()
      this.loadIssueProjectPhrase()
      this.loadIssueCategories()
      this.loadIssueReslovedResult()
      this.loadIssueProjectPriority()
      this.onProjectChange([].push(this.project))
    },
    mounted: function () {
    },
    watch: {

      'filterPanel.projects': function (value) {
        if (value.length > 1) {
          this.projectVersions.disable = true
        }
      },

      project: function () {
        this.initFilterPanel()
        this.onProjectChange([].push(this.project))
      }

    },

    components: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  @import 'ProjectIssueStatus';

  .filter-block {
    margin-top: 15px;
    padding-left: 15px;
  }

  .filter-block-title {
    padding: 0px;
  }

  .filter-block-body {
    padding: 10px;
  }
</style>
