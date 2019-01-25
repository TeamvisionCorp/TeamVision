<template>
  <div>
    <project-task-board v-if="taskViewMode === 1" :projectID="projectID" @onViewTaskItem="viewTaskItem"></project-task-board>
    <project-task-gannt v-if="taskViewMode === 2" :projectID="projectID" ></project-task-gannt>
    <project-task-create-dialog :taskID="taskItemID"></project-task-create-dialog>
    <Drawer  @on-close="onPanelClose" title="筛选分析" :value="rightSidePanelShow" :inner="true" :transfer="false" :width="30" :mask="false">
       <project-task-filter :projectID="project"></project-task-filter>
    </Drawer>
  </div>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import ProjectTaskCreateDialog from './ProjectTaskCreateDialog.vue'
  import ProjectTaskBoard from './ProjectTaskBoard.vue'
  import ProjectTaskFilter from './ProjectTaskFilter.vue'
  import ProjectTaskGannt from './ProjectTaskGannt.vue'
  import Modal from "../../../../node_modules/iview/src/components/modal/modal.vue";


  export default {
    name: 'projectTaskView',
    props: {
      projectID: {
        type: [Number,String],
        defalut: 0
      }
    },
    data () {
      return {
        columnItemHeight: 200,
        taskItemID: 0
      }
    },
    computed: {
      ...mapGetters('task', ['taskChange','taskFilterStatus','taskFilterOwners','taskFilterKeyword','taskFilters','taskGanntMaxSize']),
      ...mapGetters('projectglobal', ['projectVersion','rightSidePanelShow', 'taskViewMode']),
      versionID: function () {
        return this.projectVersion
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
        ...mapMutations('task', ['setTaskChange','setTaskGanntMaxSize']),
        ...mapMutations('projectglobal', ['setViewDialogShow','setRightPanelShow']),

        onPanelClose (){
          this.setRightPanelShow(false)
        },


        viewTaskItem (taskID)
        {
          this.setViewDialogShow(true)
          this.taskItemID = parseInt(taskID)
        }

      },
    created: function () {
    },
    mounted: function () {
    },
    watch: {
    },

    components: {
      Modal,
      ProjectTaskCreateDialog,
      ProjectTaskBoard,
      ProjectTaskFilter,
      ProjectTaskGannt
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

</style>
