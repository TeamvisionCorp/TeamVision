<template>
  <div :id="fortesting.id" :key="fortesting.id">
  <Card  :padding="0"  class="board-column-item cursor-hand">
    <div class="board-item-body">
      <div  @click="onViewFortesting" style="text-decoration: underline;color:inherit;font-size: 12px;">{{ fortesting.ProjectName}}-{{ fortesting.VersionName }} {{ fortesting.Topic }}</div>
      <div style="padding-top: 20px;">
        <Dropdown trigger="click" :transfer="true">

            <Button shape="circle" size="small" href="javascript:void(0)" style="font-size:12px;">
              <Icon type="ios-mail-outline" />
              <Icon type="ios-arrow-down"></Icon>
            </Button>
        <DropdownMenu slot="list">
          <DropdownItem>
            <Icon type="ios-trending-down" style="padding-right: 10px" />
            <a style="color: inherit" :href="'/project/'+fortesting.ProjectID+'/fortesting/'+fortesting.id+'/report/bvt'" target="_blank">BVT</a>
          </DropdownItem>
          <DropdownItem><Icon type="ios-trending-up" style="padding-right: 10px" />
            <a style="color: inherit" :href="'/project/'+fortesting.ProjectID+'/fortesting/'+fortesting.id+'/report/progress'" target="_blank">进度</a>
          </DropdownItem>
          <DropdownItem> <Icon type="ios-unlock-outline" style="padding-right: 10px" />
            <a style="color: inherit" :href="'/project/'+fortesting.ProjectID+'/fortesting/'+fortesting.id+'/report/testcomplete'" target="_blank">完成</a>
          </DropdownItem>
        </DropdownMenu>
      </Dropdown></div>
      <div style="position: absolute;bottom:2px;right:10px;font-size: 10px;color:gray">
        <Tag v-if="fortesting.DeadLineFormat"  color="default">
          {{ fortesting.DeadLineFormat }}
        </Tag>
      </div>
    </div>
    <div class="board-item-rightbar">
      <div class="board-item-avatar">
        <Avatar style="background-color:#388E8E">{{ fortesting.OwnerName }}</Avatar>
      </div>
      <!--<Badge count="10"></Badge>-->

    </div>
  </Card>
  </div>
</template>

<script>

  export default {
    name: 'ProjectFortestingItem',
    props: ['fortesting'],
    data () {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    },
    methods: {
      onViewFortesting (event) {
        this.$emit('view-fortesting', this.fortesting.id)
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
    padding-bottom: 5px;

  }

</style>
