<template>
  <div>
    <Card dis-hover :bordered="false" style="margin-top: 10px;">
      <div class="citask-card-title"><Icon type="ios-list-box-outline" /> 任务队列</div>
      <div>
           <div v-for="queue in taskQueue" :key="queue.TaskUUID" style="height: 40px;border-bottom: 1px solid #f5f7f9;padding-top: 12px">
             <span style="width:70%;display: inline-block;text-align: left; padding-left: 10px;overflow: hidden; text-overflow:ellipsis; white-space: nowrap;">
               <Icon type="ios-clock-outline" /> {{ queue.TaskName }}</span>
             <span style="width:20%;display: inline-block;">{{ queue.TriggerName }}</span>
             <Tooltip content="取消任务" style="width: 10%">
               <span style="width:20%;display: inline-block;" class="cursor-hand"  @click="cancleTask(queue.TaskID,queue.TaskUUID)"><Icon type="md-close" :size="18" style="padding-right: 5px;"></Icon></span>
             </Tooltip>
           </div>
      </div>
    </Card>
     <Card dis-hover style="margin-top: 10px;" :bordered="false">
      <div class="citask-card-title">
       <span><Icon type="md-laptop" /> Agent</span>
       <span style="margin-left: 20px;">
          <span ><Icon type="ios-ionic" /> 离线</span>
          <span style="margin-left: 20px;color:#388e8e"><Icon type="ios-ionic" /> 在线</span>
       </span>
      </div>
      <div>
        <div v-if="agent.RunningTasks.length >0" v-for="agent in agents" :key="agent.id" style="border-bottom: 1px solid #f5f7f9;padding-top: 12px">
              <div style="text-align: left">
                  <span style="padding-left: 10px; padding-right: 5px;">
                    <Icon v-if="agent.Status ===2" type="md-checkmark-circle-outline" :size="14" style="color:#388e8e"></Icon>
                    <Icon v-if="agent.Status !==2" type="ios-checkmark-circle-outline" :size="14"></Icon>
                  </span>
                  <span style="padding-right: 5px;">{{ agent.Name }}</span>
                  <!--<span style="opacity: 0.5;padding-left: 8px; padding-right: 5px;font-size: 12px; color: snow; border: 1px solid #388e8e;border-radius: 10px; background: #388e8e">VEDBuild</span>-->
              </div>
              <div v-for="task in agent.RunningTasks" style="padding-left: 20px;padding-top: 10px;">
                <span style="width:60%;display: inline-block;text-align: left; padding-left: 10px;overflow: hidden; text-overflow:ellipsis; white-space: nowrap;">
                  <span style="display: block;">{{ task.TaskName }}</span>
                  <Progress :percent="task.Process" :stroke-width="5" status="success" :hide-info="true"></Progress>
                </span>

                <Tooltip content="触发着" style="width:15%;">
                  <span style="width:100%;display: inline-block;">{{ task.TriggerName }}</span>
                </Tooltip>
                <Tooltip content="点击查看日志" style="width:15%;">
                  <span style="width:100%;display: inline-block;" class="cursor-hand" @click="showCILog(task.TaskID,task.TaskUUID,task.TQID)">日志 </span>
                </Tooltip>
                <Tooltip content="取消任务" style="width:10%;">
                  <span style="width: 100%; display: inline-block" class="cursor-hand" @click="cancleTask(task.TaskID,task.TaskUUID)"><Icon type="md-close" :size="18" style="padding-right: 5px;"></Icon></span>
                </Tooltip>
              </div>
        </div>

        <div v-if="agent.RunningTasks.length ===0" v-for="agent in agents" :key="agent.id" style="border-bottom: 1px solid #f5f7f9;padding-top: 12px">
          <div style="text-align: left">
                  <span style="padding-left: 10px; padding-right: 5px;">
                    <Icon v-if="agent.Status ===2" type="md-checkmark-circle-outline" :size="14" style="color:#388e8e"></Icon>
                    <Icon v-if="agent.Status !==2" type="ios-checkmark-circle-outline" :size="14"></Icon>
                  </span>
            <span style="padding-right: 5px;">{{ agent.Name }}</span>
            <!--<span style="opacity: 0.5;padding-left: 8px; padding-right: 5px;font-size: 12px; color: snow; border: 1px solid #388e8e;border-radius: 10px; background: #388e8e">VEDBuild</span>-->
          </div>
          <div v-for="task in agent.RunningTasks" style="padding-left: 20px;padding-top: 10px;">
                <span style="width:60%;display: inline-block;text-align: left; padding-left: 10px;overflow: hidden; text-overflow:ellipsis; white-space: nowrap;">
                 {{ task.TaskName }}</span>
            <span style="width:20%;display: inline-block;" {{ task.TriggerName }}</span>
            <span style="width:20%;display: inline-block;" class="cursor-hand" @click="showCILog(task.TaskID,task.TaskUUID,task.TQID)">日志</span>
          </div>
        </div>

      </div>

    </Card>
    <c-i-log-show-dialog :taskID="taskID" :taskUUID="taskUUID" :tqID="tqID"></c-i-log-show-dialog>
  </div>
</template>

<script>
  import store from '../../../store/index.js'
  import CILogShowDialog from './CILogShowDialog.vue'
  import { mapGetters,mapMutations} from 'vuex'

  export default {
    name: 'ciAgent',
    data () {
      return {
        taskQueue: [],
        agents: [],
        taskID: 0,
        taskUUID: '',
        tqID: 0
      }
    },
    computed: {
      ...mapGetters('citask', ['ciLogDialogShow']),
    },
    methods: {
      ...mapMutations('citask', ['setCILogDialogShow']),
      cancleTask: function (taskID, taskUUID) {
        this.$axios.get('/api/ci/task_basic/' + taskID + '/stop/?TaskUUID=' + taskUUID).then(response => {
          this.$Message.success({
            content: response.data.result.message,
            duration: 10
          })
        }, response => {
          this.$Message.error({
            content: response.data.result.message,
            duration: 10
          })

        })
      },

      showCILog: function (taskID, taskUUID, tqID) {
        this.taskID = taskID
        this.taskUUID = taskUUID
        this.tqID = tqID
        console.log(this.tqID)
        this.setCILogDialogShow(true)
      },
      loadTaskQueue: function () {
        this.$axios.get('/api/common/task_queues?Status__in=1,2,3&Command=1&TaskType__in=1,2,3,4,5').then(response => {
          this.taskQueue = response.data.result
        }, response => {

        })
        this.recivedTaskEnqueue = false
      },
      loadAgent: function () {
        this.$axios.get('/api/common/agents').then(response => {
          console.log(response)
          this.agents = response.data.result
        }, response => {

        })
      },
      onReciveTaskStatusChange: function () {
        let ws = new WebSocket('ws://'+window.location.host+'/ws/TASKSTATUSCHANGE?subscribe-broadcast&publish-broadcast&echo')
        ws.onopen = () => {
          console.log("task enqueue websocket connected")
        }
        ws.onmessage = evt =>  {
          if(evt.data !== '--heartbeat--')
          {
            setTimeout(this.loadTaskQueue,10000)
            setTimeout(this.loadAgent,10000)
          }
        }
        ws.onerror = evt =>  {
          console.error(evt)
        }
        ws.onclose = evt => {
          console.log("connection closed")
        }
      }
      },
    created: function () {
      this.loadTaskQueue()
      this.loadAgent()
      this.onReciveTaskStatusChange()
    },
    components: {
      CILogShowDialog
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .citask-card-title
  {
    margin-left: -16px;
    margin-right: -16px;
    margin-top: -10px;
    padding: 0px;
    padding-left: 15px;
    height: 30px;
    text-align: left;
    border-bottom: 1px solid #f5f7f9
  }
</style>
