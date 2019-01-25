<template>
  <div class="app-body-head-default">
  <div class="app-body-header-bar-default">
          <Row>
            <Col :lg="16" :md="14" :sm="16" :xs="16">
            <div class="app-body-header-leftbar-default">
              <ul class="app-body-head-menu">
                <router-link to="/ci/task" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
                  <a href="/ci/task"><i class="fa fa-fw  fa-bus"></i>任务</a>
                </router-link>
                <router-link to="/ci/taskflow" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
                  <a href="/ci/taskflow"><i class="fa fa-fw  fa-bus"></i>任务流</a>
                </router-link>

                <li class="app-body-head-menu-item">
                  <a href="/ci/settings/global_variable"><i class="fa fa-fw  fa-bus"></i>设置</a>
                </li>
              </ul>
            </div>
            </Col>
            <Col :lg="4" :md="4" :sm="0" :xs="0">
            <div style="padding-top:20px;height: inherit">
              <AutoComplete v-if="menuItem === 'task'" @on-search="filterCITask" size="small"  :transfer="true"  v-model="ciTaskSearchKey" icon="ios-search" placeholder="输入任务名称，查找任务！" style="width:100%">
                <div style="overflow-y: scroll;max-height:400px;">
                <div class="demo-auto-complete-item" v-for="item in projectCITasks" v-if="item.CITaskCount>0">
                  <div class="demo-auto-complete-group">
                    <span style="padding-left: 10px;"><Avatar :src="item.PBAvatar" /></span>
                    <span >{{ item.ProjectName }}</span>
                    <span >  ({{ item.CITaskCount }})</span>
                  </div>
                  <Option v-for="option in item.CITasks" v-if="option.Display" :value="option.TaskName" :key="option.ID">
                    <a :href="option.TaskHistoryURL" class="demo-auto-complete-title">{{ option.TaskName }}</a>
                    <!--<span class="demo-auto-complete-count">{{ option.TaskName }} 人关注</span>-->
                  </Option>
                </div>
                </div>
              </AutoComplete>
            </div>
            </Col>
            <Col :lg="4" :md="6" :sm="8" :xs="8">
            <div class="app-body-header-rightbar-default" style="padding-top: 15px;height: inherit">
              <span v-if="menuItem === 'task'" @click="onAddCITask"><Avatar class="cursor-hand" style="background-color: #32be77;" icon="md-add"  /></span>
              <span v-if="menuItem === 'taskflow'" @click="onAddCITaskFlow"><Avatar class="cursor-hand" style="background-color: #32be77;" icon="md-add"  /></span>
            </div>
          </Col>
          </Row>
  </div>
  </div>
</template>

<script>
import store from '../../store/index.js'
import { mapMutations} from 'vuex'

  export default {
    name: 'CIHead',
    props: ['menuItem', 'flowID'],
    data () {
      return {
         ciTaskSearchKey: '',
         projectCITasks: []
      }
    },
    methods: {
      ...mapMutations('citask', ['setCITaskCreateDialogShow','setCITaskSearchKey']),
      ...mapMutations('citaskflow', ['setCITaskFlowCreateDialogShow']),
      loadCITaskList: function () {
        this.$axios.get('/api/ci/project/my').then(response => {
          this.projectCITasks = response.data.result
        }, response => {

        })
      },
      filterCITask: function (value) {
        this.initCITaskStatus()
        this.setCITaskSearchKey(value)
        if (value.trim() !=='')
        {
          for(let i=0;i<this.projectCITasks.length;i++)
          {
            this.projectCITasks[i].CITaskCount = 0
            for(let j=0; j<this.projectCITasks[i].CITasks.length;j++)
            {
              let temp = this.projectCITasks[i].CITasks[j]
              if(temp.TaskName.toUpperCase().indexOf(value.toUpperCase())>-1)
              {
                 temp.Display = true
                 this.projectCITasks[i].CITaskCount++
              }
              else
              {
                 temp.Display = false
              }
            }
          }
        }
      },
      initCITaskStatus: function () {
        for(let i=0;i<this.projectCITasks.length;i++)
        {
          this.projectCITasks[i].CITaskCount = 0
          for(let j=0; j<this.projectCITasks[i].CITasks.length;j++)
          {
            let temp = this.projectCITasks[i].CITasks[j]
              temp.Display = true
              this.projectCITasks[i].CITaskCount++
          }
        }

      },
      onAddCITask: function () {
        this.setCITaskCreateDialogShow(true)
      },
      onAddCITaskFlow: function () {
        this.setCITaskFlowCreateDialogShow(true)
      }

    },
    created: function () {
      this.loadCITaskList()

    },
    components: {},
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import '../../components/layout/appBody';
@import '../../components/layout/appHead';
@import '../../assets/teamcat/global/less/global';
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
