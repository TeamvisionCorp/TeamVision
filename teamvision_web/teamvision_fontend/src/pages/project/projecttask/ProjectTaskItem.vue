<template>
  <div :id="task.id"  :key="task.id">
  <Card  :padding="0"  class="board-column-item" :style="'border-left: 1px solid '+task.PriorityFormator">
    <div class="board-item-body">
      <div  class="cursor-hand">
        <Checkbox @on-change="onFinishedTask" v-if="task.Status!==2" ></Checkbox>
        <span>{{ task.ChildStatus }}</span>
        <span @click="onViewTask"  style="text-decoration: underline;">
          {{ task.Title }}
        </span>
      </div>
      <div v-if="task.Status===1" style="position: absolute;bottom:5px;right:10px;font-size: 10px;">
        <Tooltip content="截止时间">
          <Tag style="height: 22px;line-height: 22px; padding: 0px 5px 0px 5px;" :color="task.DeadLineFormat.color" type="dot">{{ task.DeadLineFormat.label }}</Tag>
        </Tooltip>

      </div>
      <div v-if="task.Status===0" style="position: absolute;bottom:5px;right:10px;font-size: 10px;">
        <Tooltip content="截止时间">
          <Tag style="height: 22px;line-height: 22px; padding: 0px 5px 0px 5px;" :color="task.DeadLineFormat.color"  type="dot">
            {{ task.DeadLineFormat.label }}
          </Tag>
        </Tooltip>
      </div>
      <div  style="padding-top: 15px;" class="cursor-hand">
        <Dropdown v-if="userInfo.id===task.Creator" trigger="click" :transfer="true" placement="bottom-start">
            <Icon type="ios-list" />
          <DropdownMenu slot="list">
            <DropdownItem style="padding:2px;">
              <Icon type="ios-trash-outline"/>
              <span  @click="onDeleteTask(task.id,task.Title)" style="padding-left:10px; font-size: 10px;">删除</span>
            </DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </div>
    </div>
    <div class="board-item-rightbar">
      <div class="board-item-avatar">
        <Avatar style="background-color:#388E8E" size="small">{{ task.OwnerName }}</Avatar>
      </div>
      <!--<Badge count="10"></Badge>-->

    </div>
  </Card>
  </div>
</template>

<script>
  import store from '../../../store/index.js'
  import { mapGetters,mapMutations} from 'vuex'
  export default {
    name: 'ProjectTaskItem',
    props: ['task'],
    data () {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    },
    computed: {
      ...mapGetters(['userInfo'])

    },
    methods: {
      ...mapMutations('task', ['setTaskChange']),
      onTaskItemClick (event) {
        this.setCreateDialogShow(true)
        let taskID = event.target.getAttribute('id')
        this.taskItemID = parseInt(taskID)
      },
      onViewTask (event) {
        this.$emit('view-task', this.task.id)
      },
      onDeleteTask(taskID,taskTitle)
      {
        this.$Modal.confirm({
          title: '任务删除确认',
          content: '<p>确定要删除任务【'+taskTitle+'】</p>',
          onOk: () => {
            this.deleteTask(taskID)
          },
          onCancel: () => {
          }
        })
      },

      onFinishedTask: function (value) {
        this.$emit('finished-task', this.task.id)
      },

      deleteTask(taskID)
      {
         console.log(taskID)
        this.$axios.delete('/api/project/task/'+taskID).then(response => {
          this.setTaskChange(true)
        }, response => {
          this.setTaskChange(true)

        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .board-item-rightbar {
    display: inline-table;

  }

  .board-item-avatar {
    margin-right: 15px;
    margin-top: 10px;
  }
  .board-column-item {
    margin-bottom: 5px;
    margin-top: 5px;
    min-height: 74px;
    max-height: 200px;
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
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

</style>
