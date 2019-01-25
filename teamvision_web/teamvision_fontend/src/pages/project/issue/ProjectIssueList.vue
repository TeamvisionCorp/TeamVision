<template>
  <div>
    <Card :padding="0" :bordered="false" :shadow="false" dis-hover style="border-left: 1px solid #e4e5e7;border-top: 1px solid #e4e5e7;">

      <div style="height: 40px;border-bottom: 1px solid #e4e5e7;">
        <div style="width: 350px;padding-left: 20px;padding-top:10px;">
          <Input v-model="issueSearchKey" size="small" search placeholder="输入关键字，回车搜索" @on-search="onSearchIssue" style="padding-right: 20px;" />
          <span style="padding-right: 20px;">{{ issueListObject.count }} 个相关问题</span>
          <!--<Icon :size='20' type="md-refresh" />-->
        </div>

      </div>

      <div style="padding: 20px 20px 20px 0px;">
        <Scroll :on-reach-bottom="handleReachBottom" loading-text="拼命加载中" :height="containerHeight">
          <project-issue-item v-for="issue in issueListObject.issueData" :key="issue.id" :issue="issue" @view-issue="onIssueItemClick"></project-issue-item>
        </Scroll>
      </div>

    </Card>
  </div>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import ProjectIssueItem from './ProjectIssueItem.vue'

  export default {
    name: 'projectIssueList',
    props: {
      projectID: {
        type: [Number,String]
      },
      issueID: {
        type: [Number,String]
      }
    },
    data () {
      return {
        columnItemHeight: 200,
        issueListObject: {
          next: null,
          issueData: [],
          count: 0
        },
        issueSearchKey: ''
      }
    },
    computed: {
      ...mapGetters('issue', ['issueChange','issueFilters','searchKeyword']),
      ...mapGetters('projectglobal', ['projectVersion']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight-66
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
        ...mapMutations('issue', ['setIssueChange','setShowIssueDetail', 'setSelectIssueID','setSearchKeyword']),
        ...mapMutations('projectglobal', ['setViewDialogShow']),

        onIssueItemClick: function (issueID) {
          this.setShowIssueDetail(true)
          this.setSelectIssueID(issueID)
        },

        onSearchIssue: function (value) {
          this.setSearchKeyword(value)
          this.loadIssueList(this.project,0)
        },

        handleReachBottom: function() {
         if(this.issueListObject.next != null)
          {
            return new Promise(resolve => {
              this.$axios.get(this.issueListObject.next).then(response => {
                this.issueListObject.issueData.push(...response.data.result.results)
                this.issueListObject.next = response.data.result.next
                this.issueListObject.count = response.data.result.count
              }, response => {
              })
            })
          } else {
            this.$Message.warning({
              content: '没有更多问题了',
              duration: 10,
              closable: true
              }
            )
          }
        },

        loadIssueList: function (projectID,projectVersion) {
          let searchFilter = ''
          if (this.issueSearchKey.trim() !== '')
          {
            searchFilter = 'Title__icontains=' + this.issueSearchKey+ '&'
          }
          this.$axios.get('/api/project/' + projectID + '/version/' + projectVersion + '/issues?' + searchFilter  + this.issueFilters).then(response => {
            this.issueListObject.issueData = []
            this.issueListObject.issueData.push(...response.data.result.results)
            this.issueListObject.next = response.data.result.next
            this.issueListObject.count = response.data.result.count
          }, response => {
          })

        }
      },
    created: function () {
      this.loadIssueList(this.project,0)
    },
    mounted: function () {
    },
    watch: {

      issueChange: function (value) {
        if(value)
        {
          this.loadIssueList(this.project,0)
          this.setIssueChange(false)
        }
      },

      issueFilters: function (value) {
        this.loadIssueList(this.project,0)
        this.setIssueChange(false)
      }

    },

    components: {
      ProjectIssueItem
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">


</style>
