<template>
  <div class="app-body-head-default">
  <div class="app-body-header-bar-default">
          <Row>
            <Col :lg="16" :md="14" :sm="16" :xs="16">
            <div class="app-body-header-leftbar-default">
              <ul class="app-body-head-menu">
                <li class="app-body-head-menu-item" style="width: 50px;">
                  <Dropdown trigger="click" transfer>
                    <a   href="javascript:void(0)">
                      <!--<Tooltip content="点击切换任务流" placement="bottom-end" style="text-overflow: ellipsis;overflow: hidden;max-width: 300px;white-space:nowrap;">-->
                      <Icon type="md-reorder" :size="24"/>
                      <!--</Tooltip>-->
                    </a>
                    <DropdownMenu slot="list" style="max-height: 400px;overflow-y: scroll">
                      <DropdownItem  key="default_return">
                        <router-link to="/ci/taskflow" tag="li">
                          <a   style="text-align: left;height: 30px;display: block;padding-top:5px; color: inherit;"><Icon type="ios-exit" /> 返回任务流</a>
                        </router-link>
                      </DropdownItem>
                      <DropdownItem  v-for="flow in myTaskFlows" :key="flow.id">
                        <router-link :to="'/ci/taskflow/'+flow.id" tag="li">
                          <a style="text-align: left;height: 30px;display: block;padding-top:5px;color: inherit;"><Icon type="ios-folder"></Icon> {{ flow.FlowName }}</a>
                        </router-link>
                      </DropdownItem>
                    </DropdownMenu>
                  </Dropdown>
                </li>
                <router-link :to="'/ci/taskflow/'+flowID" tag="li"  exact active-class="app-body-head-menu-item-active" class="app-body-head-menu-item" style="width: auto;padding-left:10px;padding-right: 10px;">
                  <a>{{ currentTaskFlowName }}</a>
                </router-link>
                <!--<router-link to="/ci/taskflow" tag="li" exact-active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">-->
                  <!--<a href="/ci/taskflow"><i class="fa fa-fw  fa-bus"></i>任务流</a>-->
                <!--</router-link>-->
                <router-link :to="'/ci/taskflow/'+flowID+'/history'" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item" style="margin-left: 10px;">
                  <a href="/ci/taskflow/12/history"><i class="fa fa-fw  fa-bus"></i>执行记录</a>
                </router-link>
                <!--<li class="app-body-head-menu-item">-->
                  <!--<a href="http://teamcat.qyvideo.net/ci/settings/global_variable"><i class="fa fa-fw  fa-bus"></i>设置</a>-->
                <!--</li>-->
              </ul>
            </div>
            </Col>
            <Col :lg="4" :md="4" :sm="0" :xs="0">
            <div style="padding-top:20px;height: inherit">
              <!--<Select   v-model="selectedTaskFlow" :transfer="true" size="small" style="width:200px"  :filterable="true">-->
                <!--<Option :value="1" label="s">-->
                  <!--s </Option>-->
              <!--</Select>-->
            </div>
            </Col>
            <Col :lg="4" :md="6" :sm="8" :xs="8">
            <div class="app-body-header-rightbar-default" style="padding-top: 15px;height: inherit">
              <span  @click="onAddSection" v-if="showNewButton">
                <Tooltip content="添加工作流阶段">
                    <Avatar class="cursor-hand" style="background-color: #32be77;" icon="md-add"  />
                </Tooltip>
              </span>
            </div>
          </Col>
          </Row>
  </div>
  </div>
</template>

<script>
import store from '../../../../store/index.js'
import { mapMutations} from 'vuex'

  export default {
    name: 'CIHead',
    props: ['flowID'],
    data () {
      return {
         themeLight: 'light',
         myTaskFlows: [],
         currentTaskFlow: null,
         taskFlowName: '',
         hasTasks: false

      }
    },
    computed: {
      currentTaskFlowName: function () {
        this.loadSelectTaskFlow(this.flowID)
        return this.taskFlowName
      },
      showNewButton: function () {
        if (this.$route.name === 'ciTaskFlowItem') {
          return true
        }
        else {
          return false
        }
    }},

    methods: {
      ...mapMutations('citaskflow', ['setAddedSectionDialogShow']),
      loadMyTaskFlows: function () {
        this.$axios.get('/api/ci/task_flow/my?page_size=10000').then(response => {
          this.myTaskFlows = response.data.result.results
        }, response => {
          // error callback
        })
      },
      loadSelectTaskFlow: function (flowID) {
        this.$axios.get('/api/ci/task_flow/' + flowID + '/').then(response => {
          this.currentTaskFlow = response.data.result
          this.taskFlowName = this.currentTaskFlow.FlowName
          for(let i=0; i<this.currentTaskFlow.Sections.length;i++)
          {
             if(this.currentTaskFlow.Sections[i].CITaskIDs.length>0)
             {
               this.hasTasks = true
             }
             else
             {
               this.hasTasks = false
             }
          }
        }, response => {
          // error callback
        })
      },
      onAddSection: function () {
        this.setAddedSectionDialogShow(true)
      }

    },
    created: function () {
      this.loadMyTaskFlows()
      this.loadSelectTaskFlow(this.flowID)
    },
    components: {}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import '../../../../components/layout/appBody';
@import '../../../../components/layout/appHead';
@import '../../../../assets/teamcat/global/less/global';
.demo-auto-complete-item{
  padding: 4px 0;
  border-bottom: 1px solid #F6F6F6;
}
.demo-auto-complete-group{
  font-size: 12px;
  padding: 4px 6px;
}
.demo-auto-complete-group span{
  color: #666;
  font-weight: bold;
}
.demo-auto-complete-group a{
  float: right;
}
.demo-auto-complete-count{
  float: right;
  color: #999;
}
.demo-auto-complete-more {
  display: block;
  margin: 0 auto;
  padding: 4px;
  text-align: center;
  font-size: 12px;
}
.demo-auto-complete-title{
  color:inherit;
  padding-left:20px;
}
.task-search-itemgroup-badge
{
  background-color: #388E8E!important;
}
</style>
