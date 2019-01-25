<template>
  <div class="ci-task-container">
    <Row :gutter="16">
      <Col :lg="16" :md="16" :sm="12" :xs="24">
      <div>
           <ci-task-flow v-if="menuItem ==='taskflow'"></ci-task-flow>
           <ci-task v-if="menuItem ==='task'"></ci-task>
           <ci-task-flow-item v-if="flowID !== ''" :taskFlowID="flowID"></ci-task-flow-item>
      </div>
      </Col>
      <Col :lg="8" :md="8" :sm="12" :xs="0" :style="'height:'+agentContainerHeight+'px'+'; overflow-y:scroll;'">
      <div >
           <ci-agent></ci-agent>
      </div>
      </Col>
    </Row>
    <c-i-task-create-dialog></c-i-task-create-dialog>
    <c-i-task-flow-create-dialog></c-i-task-flow-create-dialog>
  </div>

</template>

<script>
  import store from '../../store/index.js'
  import { mapGetters,mapMutations} from 'vuex'
  import ciTaskFlow from './citaskflow/CITaskFlow.vue'
  import ciAgent from './agent/CIAgent.vue'
  import ciTask from './citask/CITask.vue'
  import ciTaskFlowItem from './citaskflow/ci_task_flow_item/CITaskFlowItem.vue'
  import CITaskCreateDialog from './citask/CITaskCreateDialog.vue'
  import CITaskFlowCreateDialog from './citaskflow/CITaskFlowCreateDialog.vue'
  export default {
    name: 'ciTaskContainer',
    props: ['menuItem', 'flowID'],
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
      taskContainerHeight: function () {
        return  this.appBodyHeight - 33
      },
      agentContainerHeight: function () {
        return this.appBodyHeight - 33
      }
    },
    components: {

      CITaskFlowCreateDialog,
      CITaskCreateDialog,
      ciAgent,
      ciTaskFlow,
      ciTask,
      ciTaskFlowItem
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .ci-task-container{
    padding-left:20px;
    padding-right:20px;

  }

</style>
