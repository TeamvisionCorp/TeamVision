<template>
  <div  style="">
    <Row>
      <Col :lg="filterPanelWidth" :md="filterPanelWidth" :sm="filterPanelWidth" :xs="0">
         <project-issue-filter :projectID="projectID"></project-issue-filter>
      </Col>
      <Col :lg="issueContainerWidth" :md=issueContainerWidth :sm="issueContainerWidth" :xs="24">
          <project-issue-list :projectID="projectID"></project-issue-list>
      </Col>
      <Drawer  :value="showIssueDetail" class-name="fdsfds" @on-close="onCloseDetailPanel" :inner="true" :transfer="false" :width="60" :mask="false">
        <div slot style=""></div>
        <project-issue-detail :issueID="selectIssueID"></project-issue-detail>
      </Drawer>
    </Row>
    <project-issue-create-dialog :projectID="projectID" :versionID="projectVersion"></project-issue-create-dialog>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import { mapGetters, mapMutations } from 'vuex'
import projectIssueFilter from './ProjectIssueFilter.vue'
import projectIssueList from './ProjectIssueList.vue'
import ProjectIssueCreateDialog from './ProjectIssueCreateDialog.vue'
import ProjectIssueItem from './ProjectIssueItem.vue'
import ProjectIssueDetail from './ProjectIssueDetail.vue'
import { axiosSync } from './ProjectIssue'

export default {
  name: 'projectIssueBoard',
  props: {
    projectID: {
      type: [Number,String],
      default: 0
    },
    issueID: {
      type: [Number,String],
      default: 0
    }
  },
  data () {
    return {
      columnItemHeight: 200,
      taskList: [],
      taskItemID: 0
    }
  },
  computed: {
    ...mapGetters('issue', ['showIssueDetail', 'selectIssueID']),
    ...mapGetters('projectglobal', ['projectVersion']),
    ...mapGetters(['appBodyHeight']),
    containerHeight: function () {
      return this.appBodyHeight - 26
    },

    issueContainerWidth: function () {
      return 24 - this.filterPanelWidth
    },

    filterPanelWidth: function () {
      if (this.showIssueDetail) {
        return 0
      } else {
        return 6
      }
    },

    project: function () {
      let result = 0
      if (this.projectID) {
        result = this.projectID
        return result
      }

    }
  },
  methods:
      {
        ...mapMutations('issue', ['setIssueChange', 'setShowIssueDetail','setSelectIssueID']),
        ...mapMutations('projectglobal', ['setViewDialogShow','setProject']),

        onCloseDetailPanel: function () {
          this.setShowIssueDetail(false)
        }
      },
  created: function () {
    if (this.issueID !== 'all' && this.issueID !== 0) {
      this.setSelectIssueID(parseInt(this.issueID))
      this.setShowIssueDetail(true)
    }
  },
  mounted: function () {
  },
  watch: {
    projectID: function (value) {
    },
    issueID: function (value) {
      console.log(value)
      if (value !== 'all' && value !== '0') {
        this.setSelectIssueID(parseInt(value))
        this.setShowIssueDetail(true)
      }
    }
  },

  components: {
    draggable,
    projectIssueFilter,
    ProjectIssueCreateDialog,
    ProjectIssueItem,
    projectIssueList,
    ProjectIssueDetail
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .board-column-item {
    margin-bottom: 5px;
    margin-top: 5px;
    min-height: 74px;
    max-height: 200px;
    width: 280px;
  }

  .board-item-priority {
    width: 1px;
    display: inline-block;
    float: left;
    height:170px;
  }

  .board-item-body {
    width: 235px;
    display: inline-table;
    word-wrap: break-word;
    white-space: initial;
    padding: 10px;

  }

  .board-item-rightbar {
    display: inline-table;
  }

  .board-item-avatar {
    margin-right: 15px;
    margin-top: 10px;
  }

  .ivu-drawer-body {
    width: 100%;
    height: calc(100% - 51px);
    padding: 0px !important;
    font-size: 12px;
    line-height: 1.5;
    word-wrap: break-word;
    position: absolute;
    overflow: auto;
  }

</style>
