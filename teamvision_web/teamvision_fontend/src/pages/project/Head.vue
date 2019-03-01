<template>
  <div class="app-body-head-default">
  <div class="app-body-header-bar-default">
    <Row>
      <i-col :lg="12" :sm="18">
        <div class="app-body-header-leftbar-default pull-left">
          <ul class="app-body-head-menu">

            <router-link :to="'/project/'+ projectID +'/issue/all'" :exact="false" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
              <a href=""><i class="fa fa-fw  fa-bug"></i>问题</a>
            </router-link>
            <router-link :to="'/project/'+projectID+'/fortesting'" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
              <span class="cursor-hand">
                  <i class="fa fa-fw  fa-bus"></i>提测
                </span>
              <!--<Dropdown transfer trigger="click">-->
              <!--<a :href="'/project/'+projectID+'/fortesting'">-->
                <!--<span>-->
                  <!--<i class="fa fa-fw  fa-bus"></i>提测-->
                <!--</span>-->
                <!--<Icon type="ios-arrow-down"></Icon>-->
              <!--</a>-->
              <!--<DropdownMenu slot="list">-->
                <!--<DropdownItem name="1"> <i class="fa fa-fw  fa-bus"></i> 提测</DropdownItem>-->
                <!--<DropdownItem name="2"><Icon type="md-recording" /> 报告</DropdownItem>-->
              <!--</DropdownMenu>-->
              <!--</Dropdown>-->

            </router-link>
            <router-link :to="'/project/'+projectID+'/task'" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
              <a :href="'h/project/'+projectID+'/task'"><Icon type="md-list" /> 任务</a>
            </router-link>
            <li class="app-body-head-menu-item">
              <a  :href="'/project/'+ projectID +'/statistics/all'"><Icon type="ios-stats"/> <span>统计</span></a>
            </li>
            <!--<router-link :to="'/project/'+projectID+'/documents'" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">-->
              <!--<a :href="'/project/'+projectID+'/documents'"><Icon type="md-albums" />文件</a>-->
            <!--</router-link>-->
            <!--<li class="app-body-head-menu-item">-->
              <!--<a  :href="'/project/'+ projectID +'/settings/basic'"><i class="fa fa-cog fa-fw"></i> <span>设置</span></a>-->
            <!--</li>-->
          </ul>

        </div>
      </i-col>
      <i-col :lg="6" :sm="0" :xs="0">
        <div class="pull-left" style="padding-top: 20px;">
          <div v-if="showVersionDropDown">

            <Select v-model="lastestVersion"  @on-change="onVersionChange" :transfer="true" size="small" style="width:200px"  :filterable="true">
              <Option v-for="item in versionList" :value="item.id" :key="item.id" :label="item.VersionLabel">
                {{ item.VersionLabel }} </Option>
            </Select>
          </div>

        </div>
      </i-col>
      <i-col :lg="6" :sm="6" :xs="6">
        <div class="app-body-header-rightbar-default pull-right">
          <span @click="newTask" v-if="showNewButton">
              <Avatar style="background-color: #32be77;"  class="cursor-hand" icon="md-add" />
          </span>
          <span @click="newTask" v-if="routerName==='projectDocument'">

            <Dropdown transfer @on-click="createDocument">
        <span>
          <Avatar style="background-color: #32be77;"  class="cursor-hand" icon="md-add" />
            <Icon type="ios-arrow-down"></Icon>
        </span>
        <DropdownMenu slot="list">
            <DropdownItem name="1"><Icon type="ios-folder" /> 文件夹</DropdownItem>
            <DropdownItem name="2"><Icon type="ios-document" /> Excel</DropdownItem>
          <DropdownItem name="3"><Icon type="ios-cloud-upload" />上传文件</DropdownItem>
        </DropdownMenu>
    </Dropdown>
          </span>
          <span v-if="routerName==='projectIssue'" style="padding-left: 10px">
             <Divider type="vertical" />
              <Tooltip content="导出" transfer>
                <a style="color:inherit" :href="'/api/project/'+ projectID +'/issue/export?Title__icontains='+searchKeyword+'&'+issueFilters"><Icon type="md-log-out" :size="20" /></a>
              </Tooltip>
          </span>
          <span v-if="routerName==='projectTask'" style="padding-left: 10px;" class="cursor-hand">
            <Dropdown transfer @on-click="taskViewSwitch">
        <a href="javascript:void(0)" style="color: inherit;">
             <Divider type="vertical" />
                <span>
                  <Icon type="md-apps" :size="24"/>
                </span>
            <Icon type="ios-arrow-down"></Icon>
        </a>
        <DropdownMenu slot="list">
            <DropdownItem name="1"><Icon type="md-podium" /> 看板</DropdownItem>
            <DropdownItem name="2"><Icon type="ios-paw" /> 甘特图</DropdownItem>
        </DropdownMenu>
        </Dropdown>
        <Divider type="vertical" />
            <span v-if="taskViewMode === 1">
                <Tooltip content="筛选" transfer v-if="taskViewMode === 1">
                <span @click="showRightPanel">
                  <Icon type="ios-funnel-outline" :size="24" />
                </span>
              </Tooltip>
            </span>
          </span>
          <Divider type="vertical" />
          <a  style="color:inherit;" :href="'/project/'+ projectID +'/settings/basic'"><Icon :size="24" type="ios-cog" /></a>
        </div>
      </i-col>
    </Row>
  </div>
  </div>
</template>

<script>
  import Select from '../../../node_modules/iview/src/components/select/select.vue'
  import Option from '../../../node_modules/iview/src/components/select/option.vue'
  import { mapMutations, mapGetters } from 'vuex'
  import ICol from '../../../node_modules/iview/src/components/grid/col.vue'

  export default {
    components: {
      ICol,
      Option,
      Select
    },
    name: 'ProjectHead',
    props: ['projectID'],
    data() {
    return {
      versionList: [],
      lastestVersion: 0,
      taskViewMode: 1
    }
  },

  computed: {
    ...mapGetters('issue', ['issueFilters','searchKeyword']),
      showVersionDropDown: function () {
        if (this.$route.name === 'projectTask' || this.$route.name === 'projectFortesting' || this.$route.name === 'projectPlan') {
          return true
        }
        else {
          return false
        }
      },
    showNewButton: function () {
      if ( this.$route.name === 'projectFortesting' || this.$route.name === 'projectPlan' ||this.$route.name === 'projectIssue') {
         return true
      } else {
        if (this.$route.name === 'projectTask' && this.taskViewMode === 1) {
          return true
        } else {
          return false
        }
      }
    },
    routerName: function () {
      return this.$route.name
    },
    activeFab: function () {
      switch (this.tabs) {
        case 'one': return { 'class': 'purple', icon: 'account_circle' }
        case 'two': return { 'class': 'red', icon: 'edit' }
        case 'three': return { 'class': 'green', icon: 'keyboard_arrow_up' }
        default: return {}
      }
    }
  },
  methods: {
    ...mapMutations('task', ['setTaskGanntMaxSize']),
    ...mapMutations('projectglobal',['setCreateDialogShow','setProjectVersion','setRightPanelShow', 'setTaskViewMode','setCreateDocumentType']),
    newTask () {
      this.setCreateDialogShow(true)
    },
    onVersionChange (value) {
      console.log(value)
      this.setProjectVersion(value)
    },

    showRightPanel () {
      this.setRightPanelShow(true)
    },

    taskViewSwitch (value) {
      this.setTaskViewMode(parseInt(value))
      this.taskViewMode = parseInt(value)
    },

    createDocument: function (value) {
      this.setCreateDocumentType(parseInt(value))
    },

    maxSizeGannt: function () {
      this.setTaskGanntMaxSize(true)
    },
    loadProjectVersions: function () {
      this.$axios.get('/api/project/' + this.projectID + '/detail?extinfo=1').then(response => {
        console.log(response)
        let versions = response.data.result.Versions
        this.versionList = []
        if( versions.length > 0)
        {

          this.versionList.push(...versions)
          this.lastestVersion = versions[0].id
          this.setProjectVersion(this.lastestVersion)
        }
      }, response => {

      })
    }
  },
  created: function () {
    this.loadProjectVersions()
  },

  watch: {
      projectID: function () {
        this.loadProjectVersions()
      },
    top: function (val) {
      this.bottom = !val
    },
    right: function (val) {
      this.left = !val
    },
    bottom: function (val) {
      this.top = !val
    },
    left: function (val) {
      this.right = !val
    }
  }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import '../../components/layout/appBody';
@import '../../components/layout/appHead';
@import '../../assets/teamvision/global/less/global';

</style>
