<template>
  <div>
    <Card  v-for="taskFlow in taskFlowList" :key="taskFlow.flowID" class="env_archive_folder" :padding="0">
      <div class="env_archive_folder_header">
        <span class="pull-right" style="color:#f0f0f0;padding:5px;" >
      <Dropdown @on-click="flowContextMenuClick">
        <i class="fa fa-bars fa-fw"></i>
        <DropdownMenu slot="list">
            <DropdownItem :name="'rename:'+taskFlow.flowID" style="height: 20px;padding-top: 2px;text-align: left">
              <span style="margin-right: 5px;">
                <Icon type="md-create"></Icon>
              </span>
              <span>重命名</span>
            </DropdownItem>
            <DropdownItem :name="'copy:'+taskFlow.flowID" style="height: 20px;padding-top: 2px;text-align: left">
              <span style="margin-right: 5px;">
                <Icon type="ios-copy"></Icon>
              </span>
              <span>复制</span>
            </DropdownItem>
             <DropdownItem :name="'delete:'+taskFlow.flowID" style="height: 20px;padding-top: 2px; text-align: left">
              <span style="margin-right: 5px;">
                <Icon type="ios-trash"></Icon>
              </span>

              <span>删除</span>
            </DropdownItem>
        </DropdownMenu>
    </Dropdown>
        </span>
      </div>
      <div class="env_archive_folder_body">
        <a v-if="taskFlow.taskFlowNameView" :href="'/ci/taskflow/'+taskFlow.flowID"  style="border:none;background-color: inherit;argin-right:auto;margin-left:auto;width:80%;margin-top:10px;font-size:6px;">
		                  <span class="task-flow-title cursor-hand" style="width:100%;text-decoration: underline;">
		                    {{ taskFlow.flowName }}
		                  </span>
        </a>
        <div v-if="taskFlow.taskFlowNameEdit">
            <Input name="taskFlowName" v-model="taskFlow.flowName" size="small" :maxlength="50" :autofocus="true" @on-blur="flowNameEditComplete" style="width: auto;padding-top: 25px;padding-left: 30px"></Input>
        </div>
      </div>
      <div class="env_archive_folder_footer">
        <center>
          <div class="env_archive_version_file">
            <div  href="#"  style="color: inherit;">
              <Tooltip content="执行">
                <span @click="onStartTaskFlow(taskFlow.flowID)"><Icon type="md-play" :size="18" color="#555"></Icon></span>
              </Tooltip>
              <!--<Tooltip content="取消">-->
                <!--<Icon type="stop" :size="18" color="#555" style="margin-left: 10px;"></Icon>-->
              <!--</Tooltip>-->
              <!--<Tooltip content="配置">-->
                <!--<Icon type="android-settings" :size="18" color="#555" style="margin-left: 10px;"></Icon>-->
              <!--</Tooltip>-->

            </div>
          </div>
          <div style="font-size:12px; margin-top: 6px;" v-if="taskFlow.lastRunTime">
            <Tooltip content="上次执行时间">
              <span style="margin-top:0px;margin-left: 0px;" class=""><Icon type="ios-checkmark-circle" style="color:#388e83"></Icon> {{ taskFlow.lastRunTime }}</span>
            </Tooltip>
          </div>
        </center>

      </div>
    </Card>
  </div>
</template>

<script>
  import store from '../../../store/index.js'
  import { mapGetters,mapMutations} from 'vuex'
  export default {
    name: 'ciTaskFlow',
    data () {
      return {
        taskFlows: [],
        editFlow: 0
      }
    },
    computed: {
      ...mapGetters('citaskflow', ['ciTaskFlowAdded']),
      taskFlowList: function () {
         if(this.ciTaskFlowAdded)
         {
           this.loadTaskFlows()
           this.setCITaskFlowAdded(false)
         }
         return this.taskFlows
      }
    },
    methods: {
      ...mapMutations('citaskflow',['setCITaskFlowCreateDialogShow', 'setCITaskFlowAdded']),
      flowContextMenuClick: function (itemCommand) {
        let commandArray = itemCommand.split(':')
        let command = commandArray[0]
        let commandParameter = commandArray[1]
        this.editFlow = commandParameter
        if(command === 'rename')
        {
          for(let i=0;i<this.taskFlowList.length; i++)
          {
             if(this.taskFlowList[i].flowID+'' === commandParameter)
             {
               this.taskFlowList[i].taskFlowNameEdit = true
               this.taskFlowList[i].taskFlowNameView = false
               break
             }
          }

        }

        if(command === 'copy')
        {
           this.copyTaskFlow(commandParameter)
        }

        if(command === 'delete')
        {
          let flowName = this.findTaskFlow(commandParameter).flowName
          this.$Modal.confirm({
            title: '删除确认',
            content: '<p>删除是危险操作，确认要删除任务流 ['+flowName+' ] 吗？</p>',
            onOk: () => {
              this.deleteTaskFlow(commandParameter)
            },
            onCancel: () => {
            }
          });

        }
      },

      findTaskFlow: function (flowID) {
        let result = null
        for(let i=0;i<this.taskFlowList.length; i++)
        {
          if(this.taskFlowList[i].flowID+'' === flowID)
          {
            result = this.taskFlowList[i]
            break
          }
        }
        return result
      },

      copyTaskFlow: function (flowID) {
        this.$axios.get('/api/ci/task_flow/' + flowID+'/copy').then(response => {
          this.loadTaskFlows()
        }, response => {
          // error callback
        })
      },

      deleteTaskFlow: function (flowID) {
        this.$axios.delete('/api/ci/task_flow/' + flowID).then(response => {
          this.loadTaskFlows()
        }, response => {
          // error callback
        })
      },

      flowNameEditComplete: function () {
        for(let i=0;i<this.taskFlowList.length; i++)
        {
          if(this.taskFlowList[i].flowID+'' === this.editFlow)
          {
            this.taskFlowList[i].taskFlowNameEdit = false
            this.taskFlowList[i].taskFlowNameView = true
            this.updateTaskFlowName(this.editFlow,this.taskFlowList[i].flowName)
            this.editFlow = 0
            break
          }
        }
      },

      loadTaskFlows: function () {
        this.$axios.get('/api/ci/task_flow/my?page_size=10000').then(response => {
          let taskFlowList = response.data.result.results
          this.taskFlows = []
          for (let i = 0; i < taskFlowList.length; i++)
          {
            this.taskFlows.push({
              flowID: taskFlowList[i].id,
              flowName: taskFlowList[i].FlowName,
              lastRunTime: taskFlowList[i].LastRunTime,
              taskFlowNameEdit: false,
              taskFlowNameView: true
            })
          }

        }, response => {
          // error callback
        })
      },
      updateTaskFlowName: function (flowID,name) {
        this.$axios.patch('/api/ci/task_flow/' + flowID + '/',{'FlowName': name}).then(response => {
        }, response => {
          // error callback
        })
      },

      onStartTaskFlow: function (flowID) {
        this.$axios.get('/api/ci/task_flow/' + flowID + '/start').then(response => {
          this.$Message.success({
            content: response.data.result.message,
            duration: 10
          })
        }, response => {
        })
      }
    },
    created: function () {
      this.loadTaskFlows()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .env_archive_folder
  {
    border:1px solid #f0f0f0;
    width:250px;
    height:150px;
    margin:10px 10px 10px 30px;
    border-radius:5px;
    cursor:pointer;
    float: left;
    padding:0px;
  }

  .env_archive_folder_header
  {
    height:0px;
  }

  .env_archive_folder_body
  {
    height:90px;
  }

  .env_archive_folder_body center
  {
    padding-top: 10px;
    color:#d3d7d4;
  }

  .env_archive_folder_footer
  {
    border-top:1px solid #f0f0f0;
    height:50px;
  }

  .env_archive_folder_version
  {
    padding:10px 5px 5px 5px;
    font-size: 14px;
    color: black;
    overflow:hidden;

  }

  .env_archive_version_file
  {
    padding:5px 5px 0px 5px;
    font-size: 14px;
    color: black;
    overflow:hidden;

  }

  .task-flow-title{
    height: 80px;
    width: 80px;
    line-height: 80px;
    display:inline-block;
    color: #5e5e5e;
    text-align:center;
  }
</style>
