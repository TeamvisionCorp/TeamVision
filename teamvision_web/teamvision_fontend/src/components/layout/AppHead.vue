<template>
  <div id="app-head" class="app-head master-page-header-font">
    <Row>
      <i-col :lg="1" :md="2" :sm="2" :xs="2" class="app-head-logo app-head-item">
        <a href="/home"><img src="../../assets/teamcat/global/images/logo.jpg" class="img-circle"
                             style="width: 40px; height: 40px;"></a>
      </i-col>
      <i-col :lg="1" :md="1" :sm="0" :xs="0" class="app-head-title">
        TeamVision
      </i-col>
      <i-col id="headermenu" :lg="15" :md="12" :sm="16" :xs="16" class="app-head-menu app-head-item">
        <ul class="list-inline">

          <router-link to="/home/summary" tag="li" active-class="app-head-menu-item-active" id="header_menu_home"
                       class="app-head-menu-item">
            <a href="/home/summary">
              <Icon type="home"></Icon>
              我的</a>
          </router-link>
          <router-link to="/project" tag="li" active-class="app-head-menu-item-active" id="header_menu_project"
                       class="app-head-menu-item">
            <a href="/project"><i class="fa fa-fw  fa-bus"></i>项目</a>
          </router-link>


          <router-link to="/ci" tag="li" active-class="app-head-menu-item-active" id="header_menu_project"
                       class="app-head-menu-item">
            <a href="/ci"><i class="fa fa-fw  fa-building-o"></i>CI</a>
          </router-link>
          <!--<router-link to="/interface" tag="li" active-class="app-head-menu-item-active" id="header_menu_env"-->
                       <!--class="app-head-menu-item">-->
            <!--<a href="/interface"><i class="fa fa-fw  fa-bus"></i>API</a>-->
          <!--</router-link>-->
        </ul>
      </i-col>
      <i-col v-if="showProject" :lg="3" :md="3" :sm="0" :xs="0">
        <ul class="list-inline">
          <li name="header_menu_device" label="device" labelid="3" class="app-head-menu-item cursor-hand" style="padding-top: 25px;">
            <Dropdown trigger="click">
               <span style="color:#fff" ><Avatar :src="projectInfo.PBAvatar" size="small" />
              <span style="padding-left:5px;">{{ projectInfo.PBTitle }}</span>
              <span><Icon :size="24" type="md-arrow-dropdown" /></span>
            </span>
              <DropdownMenu slot="list" style="max-height: 400px;overflow-y: scroll;color:#5e5e5e;">
                <DropdownItem  v-for="project in myProjects" :key="project.id">
                  <router-link :to="{ name: router.name, params: { projectID: project.id }}" tag="li">
                    <a href="#"  style="text-align: left;height: 30px;display: block;padding-top:5px;color:inherit">
                      <span ><Avatar :src="project.PBAvatar" size="small" />
                        <span style="padding-left:5px;">{{ project.PBTitle }}</span>
                      </span>
                    </a>
                  </router-link>
                </DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </li>
        </ul>
      </i-col>
      <i-col id="headersettings" :lg="2" :md="4" :sm="4" :xs="4" class="pull-right app-head-settings app-head-item">
        <!--<ul class="list-inline">-->
        <!--<li id="admin_board"><i class="fa fa-cogs fa-fw fa-lg"></i></li>-->
        <!--<li id="loginuser"><i class="fa fa-user-o fa-fw fa-lg"></i></li>-->
        <!--</ul>-->
        <Dropdown v-if="systemPermission < 3">
          <i style="font-size:16px;opacity:0.6;" class="fa fa-cogs fa-fw fa-lg cursor-hand"></i>
          <DropdownMenu slot="list">
            <DropdownItem><a style="color:#333" href="/administrate/user/all">
              <i class="fa fa-user fa-fw fa-lg"></i> 用户</a></DropdownItem>
            <DropdownItem><a style="color:#333" href="/administrate/device/all">
              <i class="fa fa-mobile fa-fw fa-lg"></i> 设备</a></DropdownItem>

          </DropdownMenu>
        </Dropdown>
        <Dropdown style="margin-left: 20px" placement="bottom-end">
          <i style="font-size:16px;opacity:0.6;" class="fa fa-user-o fa-fw fa-lg cursor-hand"></i>
          <DropdownMenu slot="list">
            <DropdownItem><a style="color:#333" :href="'/ucenter/'+ userID +'/account/basic'"><i
              class="fa fa-home fa-fw pull-left"></i>个人中心</a></DropdownItem>
            <DropdownItem divided><a style="color:#333" href="/user/logout">
              <i class="fa fa-sign-out fa-fw pull-left"></i>注销</a></DropdownItem>
          </DropdownMenu>
        </Dropdown>
      </i-col>

    </Row>
  </div>

</template>

<script>
  import store from '../../store/index.js'
  import { mapGetters, mapMutations } from 'vuex'
  import ICol from '../../../node_modules/iview/src/components/grid/col.vue'

  export default {
    components: {ICol},
    name: 'AppHead',
    data () {
      return {
        systemPermission: 99,
        userID: 0,
        showHeadProject: false,
        projectID: 0,
        projectInfo: null,
        myProjects: [],
        router: null
      }
    },
    computed: {
      ...mapGetters(['menuLabelID']),

      showProject: function () {
        return this.showHeadProject
      }
    },
    methods:
      {
        ...mapMutations(['setUserInfo']),
        loadUserInfo: function () {
          this.$axios.get('/api/common/user/0').then(response => {
            if (response.data.result.id !=null)
            {
              this.systemPermission = response.data.result.system_permision
              this.userID = response.data.result.id
              this.setUserInfo(response.data.result)
            } else {
              if (this.$route.name !== 'projectIssueMobileUpload') {
                window.location = '/user/login'
              }
            }
          }, response => {
          })
          },
        loadProjectInfo: function () {
          if(this.projectID !==0)
          {
            this.$axios.get('/api/project/'+ this.projectID +'/detail?extinfo=0').then(response => {
              this.projectInfo = response.data.result
            }, response => {
            })

          }
        },
        loadMyProject: function () {
          this.$axios.get('/api/project/list?extinfo=0&home=1').then(response => {
            this.myProjects = response.data.result
          }, response => {
          })
        },
      },
    created: function () {
      this.loadUserInfo()
      this.loadProjectInfo()
      this.loadMyProject()
    },
    mounted: function () {
    },
    watch: {
      '$route' (to, from) {
        if (to.name !== 'projectRoot' && to.name.indexOf('project') > -1) {
          console.log(to)
          this.showHeadProject = true
          this.projectID = to.params.projectID
          this.router = to
        }
        else {
          this.showHeadProject = false
          this.projectID = 0
        }
      },
      projectID: function () {
        this.loadProjectInfo()
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  @import "appHead";
</style>
