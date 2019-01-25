<template>
  <div>
  <Card class="citask-card" :bordered="false">
    <div class="citask-card-title">
      <a v-if="item.IsActive" style="color: inherit;text-decoration:underline;" target="_self" :href="item.TaskHistoryURI">
        #{{ item.BuildVersion }} {{ item.TaskName }}
      </a>
      <a v-if="item.IsActive ===false " style="color: inherit;text-decoration:underline;" href="#">
        #{{ item.BuildVersion }} {{ item.TaskName }}
      </a>
      <span class="pull-right" style="margin-right: 10px;">
        <span v-if="item.IsActive === false">
          <Tooltip content="记录已清除">
             <Icon type="ios-information-circle-outline" />
        </Tooltip>
        </span>
      </span>
    </div>
    <div class="citask-card-body">
        <span style="width: 220px;display: inline-block;text-align: left">
          <span style="margin-top: 25px;margin-left: 0px;">
            <Icon v-if="item.BuildStatus ===1" type="ios-checkmark-circle" style="color:#388e83"></Icon>
            <Icon v-if="item.BuildStatus ===2" type="ios-close-circle" style="color:darkred"></Icon>
            <Icon v-if="item.BuildStatus ===3" type="ios-remove-circle" style="color:olive"></Icon>
            <Icon v-if="item.BuildStatus ===0" type="ios-remove-circle" style="color:cornflowerblue"></Icon>
            {{ item.StartTimeFormatString }} </span>
        </span>
      <span style="width:80px;margin-top:25px; display: inline-block">
        <a v-if="item.BuildStatus!==0 && item.BuildLog!==''"  :href="item.BuildLog" target="_blank" style="color: inherit; text-decoration: underline;">日志</a>
        </span>
    </div>

  </Card>
  </div>
</template>

<script>
  export default {
    name: 'ciTaskHistoryItem',
    props: ['item'],
    data () {
      return {
        msg: ''
      }
    },
    methods: {
      onDPItemClick (itemID) {
        let taskStartParameters = itemID.split(',')
        this.$axios.get('/api/ci/task_basic/' + taskStartParameters[1] + '/start/?BuildParameter=' + taskStartParameters[0]).then(response => {
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
      onBuildClick (taskID) {
        this.$axios.get('/api/ci/task_basic/' + taskID + '/start/').then(response => {
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
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .citask-card{
    width: 350px;
    height: 100px;
    float: left;
    margin-left: 10px;
    margin-top: 10px;
  }
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
  .citask-card-body{

  }
</style>
