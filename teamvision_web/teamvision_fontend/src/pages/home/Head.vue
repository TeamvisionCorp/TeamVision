<template>
  <div class="app-body-head-default">
    <div class="app-body-header-bar-default">
      <div class="app-body-header-leftbar-default pull-left">
        <ul class="app-body-head-menu">

          <router-link to="/home/summary" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
            <a href="/home/summary"><i class="fa fa-fw  fa-bus"></i>面板</a>
          </router-link>
          <!--<li class="app-body-head-menu-item">-->
            <!--<a  href="/home/project/all"><i class="fa fa-flag fa-fw fa-lg"></i> <span>项目</span></a>-->
          <!--</li>-->
          <router-link to="/home/my/issue" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
            <a href="#"><i class="fa fa-fw  fa-bug"></i>问题</a>
          </router-link>
          <router-link to="/home/my/fortesting" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
            <a href="#"><i class="fa fa-fw  fa-flag"></i>提测</a>
          </router-link>
          <router-link to="/home/my/task" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
            <a href="/home/my/task"><i class="fa fa-fw  fa-bus"></i>任务</a>
          </router-link>
          <li name="header_menu_device" label="device" labelid="3" class="app-body-head-menu-item">
            <a href="/home/device/all"><i class="fa fa-fw fa-lg fa-mobile"></i>设备</a>
          </li>
          <li class="app-body-head-menu-item">
            <a  href="/home/webapps/all"><i class="fa fa-flag fa-fw fa-lg"></i> <span>工具</span></a>
          </li>
        </ul>
    </div>
      <div class="app-body-header-rightbar-default pull-right">
            <span @click="newTask"  v-if="showNewButton">
              <Avatar style="background-color: #32be77;"  class="cursor-hand" icon="md-add" />
            </span>
        <span v-if="routerName==='homeIssue'" style="padding-left: 10px">
             <Divider type="vertical" />
              <Tooltip content="导出" transfer="">
                <a style="color:inherit" :href="'/api/project/0/issue/export?Title__icontains='+searchKeyword+ '&' +issueFilters"><Icon type="md-log-out" :size="20" /></a>
              </Tooltip>
          </span>
        <span v-if="routerName==='homeTask'" style="padding-left: 10px;" class="cursor-hand">
             <Divider type="vertical" />
              <Tooltip content="筛选" transfer>
                <span @click="showRightPanel">
                  <Icon type="ios-settings-outline" :size="24"/>
                </span>
              </Tooltip>
          </span>
      </div>
  </div>
  </div>
</template>

<script>
  import { mapMutations,mapGetters } from 'vuex'
  export default {
    name: 'MyHead',
    computed: {
      ...mapGetters('issue', ['issueFilters','searchKeyword']),

      showNewButton: function () {
        if (this.$route.name === 'homeTask' || this.$route.name === 'homeFortesting' || this.$route.name === 'homeIssue') {
          return true
        }
        else {
          return false
        }
      },
      routerName: function () {
        return this.$route.name
      }
    },
    methods: {
    ...mapMutations('projectglobal',['setCreateDialogShow','setRightPanelShow']),
      newTask () {
        this.setCreateDialogShow(true)
      },
      showRightPanel () {
        this.setRightPanelShow(true)
      },
    },
    mounted: function () {
      this.setRightPanelShow(false)
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import '../../components/layout/appBody';
@import '../../assets/teamcat/global/less/global';
</style>
