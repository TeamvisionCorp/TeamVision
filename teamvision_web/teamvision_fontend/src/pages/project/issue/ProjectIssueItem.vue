<template>
  <div  :class="'project_issue_listview_item cursor-hand ' + issueActiveClass" @click="onIssueClick(issue.id)" >
      <div class="row">
        <i-col :span="24">
          <div class="project_issue_listview_item_title">
            <i-col :span="24">
              <Tooltip content="严重性" transfer>
                <i :class="'fa fa-circle fa-fw ' + issue.severity_name.LabelStyle "></i>
              </Tooltip>

              <Tooltip content="问题ID">
                <span class="issue-id">#{{ issue.id }} </span>
              </Tooltip>
              <span class="issue-title">
              <span name="issue_defalut_title"> {{ issue.default_title }} </span>
              <span name="issue_real_title"> {{ issue.Title }} </span>
            </span>
            </i-col>
          </div>
          <div class="project_issue_listview_item_content row">
            <div class="col-sm-12">
            <span class="issue-content">
              <Tooltip content="问题状态">
                <i class="fa fa-eye gray"></i>
                <span :class=" issue.status_name.LabelStyle"> {{ issue.status_name.Name }} </span>
              </Tooltip>
            </span>
              <span class="issue-content">
              <Tooltip content="创建人">
                <span><i class="fa fa-user"></i>  {{ issue.creator_name }} </span>
              </Tooltip>
            </span>
              <span class="issue-content">
              <Tooltip content="经办人">
                 <span class="gray "><i class="fa fa-hand-o-right"></i>  {{ issue.processor_name }} </span>
              </Tooltip>
            </span>

              <span class="issue-content">
              <Tooltip content="模块名称">
                <span> <i class="fa fa-cube"></i>  {{ issue.module_name }} </span>
              </Tooltip>
            </span>
              <span class="issue-content">
              <Tooltip content="版本">
                <span><i class="fa fa-code-fork"></i>  {{ issue.version_name }} </span>
              </Tooltip>
            </span>
              <span class="issue-content">
              <Tooltip content="创建日期">
                <span> <i class="fa fa-clock-o"></i>  {{ issue.create_date }} </span>
              </Tooltip>
            </span>
              <span class="issue-content">
              <Tooltip content="解决结果">
                <span><i :class="'fa ' + issue.solution_name.Label+' ' +issue.solution_name.LabelStyle "></i> {{ issue.solution_name.Name }}</span>
              </Tooltip>
            </span>
            </div>
          </div>
        </i-col>
      </div>
  </div>

</template>

<script>

import {mapGetters, mapMutations} from 'vuex'

export default {
  name: 'ProjectIssueItem',
  props: ['issue'],
  data () {
    return {
    }
  },

  computed: {
    ...mapGetters('issue', ['selectIssueID']),

    issueActiveClass: function () {
      if (this.issue.id === this.selectIssueID) {
        return 'project_issue_selected_item'
      } else {
        return ''
      }
    }

  },
  methods: {
    onIssueClick (id) {
      this.$emit('view-issue', id)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  @import '../../../assets/teamcat/global/less/global';

  .project_issue_listview_item {
    .listview-item(80px);
    margin-left: 20px;
  }

  .project_issue_selected_item {
    background-color: #337ab7;
  }

  .project_issue_selected_item span {
    color: white;
  }


  .project_issue_listview_item_title {
    padding: 3px 0px 0px 3px;
    margin: 5px 50px 5px 10px;
    height: 22px;
    line-height: 28px !important;
  }

  .project_issue_listview_item_content {
    padding-top: 8px;
    color: #555;
    margin-left: 0px;
    display: block;
    line-height: 20px;
    font-size: 14px;
  }

  .project_issue_status {
    width: 2px;
    height: 78px;
    float: left;
    opacity: 0.6;
    margin-top: -5px;
    margin-bottom: 3px;
  }


  .issue-item {
    padding-right: 0px !important;
    padding-left: 0px !important;
    margin-left: -1px;
  }

  .issue-item-panel {
    background-color: none;
    border: none;
    box-shadow: none;
    margin-bottom: 25px;
  }

  .issue-item-panel-head {
    border-top-width: 3px;
    height: 40px;
    background: #fff;
    border-color: #e4e5e7;
    border: 1px solid #e4e5e7;
    padding: 10px 10px;
    border-radius: 0px;
  }

  .issue-item-panel-head-tools {
    display: inline-block;
    float: right;
    margin-top: 0;
    padding: 0;
    position: relative;

  }


  .issue-item-panel-body {
    background: #fff;
    border: 1px solid #e4e5e7;
    border-top: none;
    border-radius: 0px;
    padding: 20px;
    position: relative;
    overflow-y: scroll;
  }

  .issue-item-panel-footer {
    color: inherit;
    border: 1px solid #e4e5e7;
    border-top: none;
    font-size: 90%;
    background: #f7f9fa;
    padding: 10px 15px;
    border-radius: 0px;
  }

  .issue-detail-operation {
    font-size: 14px;
    padding: 5px 10px 5px 10px;
    margin: 5px 5px 5px 5px;
    border: 1px solid #b2b2b2;
    border-radius: 15px;
  }

  .md-toolbar {
    padding: 10px;
    border: 1px solid #d8d8d8;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
  }

  .issue-content {
    display: inline-block;
    margin-left: 20px;
    color: #b2b2b2;
  }

  .issue-title {
    font-weight: 500;
    color: #3b73af;
    font-size: 14px !important;
    margin-left: 20px;
  }

  .issue-id {
    margin-left: 20px;
    color: #3b73af;
  }

  .issue-status-fresh {
    color: #8b7cc5;
  }

  .issue-status-new {
    color: #45be95;
  }

  .issue-status-closed {
    color: #bedad3;
  }

  .issue-status-resolved {
    color: #5bc0de;
  }

  .issue-status-reopen {
    color: #f1494e;
  }


  .issue-severity-fatal {
    color: #f1494e;
  }

  .issue-severity-critical {
    color: #f28033;
  }

  .issue-severity-major {
    color: #FEBC11;
  }

  .issue-severity-minor {
    color: #55ccf4;
  }

  /*问题动态设置------------------------------------------------------------*/
  .issue-detail-activity {
    border-top: 1px solid #f2f2f2;
    background-color: #f8f9fa;
  }

  .issue-detail-activity-title {
    margin-bottom: 2px;
    color: #b2b2b2;
    padding: 15px 5px 5px 30px;
  }

  .issue-detail-comment-add {
    width: 60%;
    height: 47px;
    background-color: #FFFFFF;
    position: fixed;
    bottom: 0px;
    border-top: 1px solid #f2f2f2;
    border-bottom: 1px solid #f2f2f2;
  }

  .issue-comment-add-button {
    background-color: #3f5872;
    border-color: #3f5872;
    color: #FFFFFF;

  }

</style>
