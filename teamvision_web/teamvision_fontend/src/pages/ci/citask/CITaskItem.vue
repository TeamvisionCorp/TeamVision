<template>
  <div>
  <Card class="citask-card" v-if="item.Display" :bordered="false">
    <div class="citask-card-title">
      <a style="color: inherit;text-decoration:underline;" :href="item.TaskHistoryURI">
        {{ item.TaskName }}
      </a>
      <span class="pull-right" style="padding-right: 10px">
          <a :href="item.TaskConfigURI"><Icon type="ios-settings" :size="18" color="#555" style="margin-left: 10px;"></Icon></a>
      </span>
    </div>
    <div class="citask-card-body">
        <span style="width: 220px;display: inline-block;text-align: left">
          <span style="margin-top: 25px;margin-left: 0px;">
            <Icon v-if="item.LastRunStatus ===1" type="ios-checkmark-circle" style="color:#388e83"></Icon>
            <Icon v-if="item.LastRunStatus ===2" type="ios-close-circle" style="color:darkred"></Icon>
            <Icon v-if="item.LastRunStatus ===3" type="ios-remove-circle" style="color:olive"></Icon>
            {{ item.LastRunTime }} </span>
        </span>
      <span style="width:80px;margin-top:25px; display: inline-block">
        <Dropdown v-if="item.ParameterGroups.length > 0" trigger="click" @on-click="onDPItemClick" >
          <Button type="default"  shape="circle" style="padding: 3px 15px;">
            构建
            <Icon type="md-arrow-dropdown" />
          </Button>
         <DropdownMenu slot="list" style="max-height: 500px;overflow-y: scroll;top:0px;">
            <DropdownItem v-for="dpitem in item.ParameterGroups" :key="dpitem.id" :name="dpitem.id+','+item.id" ><Icon v-if="dpitem.default" type="checkmark-round"></Icon> {{ dpitem.title }}</DropdownItem>
         </DropdownMenu>
         </Dropdown>
          <Button v-if="item.ParameterGroups.length ===0" type="default"  shape="circle" @click="onBuildClick(item.id)" style="padding: 3px 15px;">
            构建
        </Button>
        </span>
    </div>

  </Card>
  </div>
</template>

<script>
  export default {
    name: 'ciTaskItem',
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
