<template>
  <div class="app-body-head-default">
  <div class="app-body-header-bar-default">
          <Row>
            <Col :lg="16" :md="14" :sm="8" :xs="2">
            <div class="app-body-header-leftbar-default">
              <ul class="app-body-head-menu">

              </ul>
            </div>
            </Col>
            <Col :lg="4" :md="4" :sm="8" :xs="10">
            <div style="padding-top:20px;height: inherit">
              <AutoComplete  @on-search="filterProjectList" size="small"  :transfer="true"  v-model="projectSearchKey" icon="ios-search" placeholder="输入项目名称，查找项目！" style="width:100%">
                <div style="overflow-y: scroll;max-height:400px;">
                  <div class="project-search-item" v-for="item in myProjectList" v-if="item.Display">
                    <a :href="'/project/'+ item.id +'/issue/all'" style="color:inherit">
                      <span class="project-search-item-title"><Avatar :src="'http://teamcat.qyvideo.net/'+item.PBAvatar" /></span>
                      <span class="project-search-item-title">{{ item.PBTitle }}</span>
                    </a>

                  </div>
                </div>
              </AutoComplete>
            </div>
            </Col>
            <Col :lg="4" :md="6" :sm="8" :xs="12">
            <div class="app-body-header-rightbar-default" style="padding-top: 15px;height: inherit">
              <span @click="addProject" class="cursor-hand"><Avatar style="background-color: #32be77;" icon="md-add" /></span>
            </div>
          </Col>
          </Row>
  </div>
  </div>
</template>

<script>
import store from '../../store/index.js'
import { mapMutations } from 'vuex'

  export default {
    name: 'CIHead',
    props: ['menuItem'],
    data (){
      return {
         myProjects: [],
         projectSearchKey: ''
      }
    },
    computed: {
         myProjectList: function () {
           return this.myProjects
         }
    },
    methods: {
      ...mapMutations('project',['setProjectCreateDialogShow','setProjectSearchKey']),
      loadMyProject: function () {
        this.$axios.get('/api/project/list?extinfo=0&home=1').then(response => {
          this.myProjects = response.data.result
        }, response => {
        })
      },
      filterProjectList: function (value) {
        this.initProjectDisplayStatus()
        this.setProjectSearchKey(value)
        for(let i=0; i<this.myProjects.length;i++)
        {
          let temp = this.myProjects[i]
          if(temp.PBTitle.toUpperCase().indexOf(value.toUpperCase())<0)
          {
             temp.Display = false
          }
        }
      },
      initProjectDisplayStatus: function () {
        for(let i=0; i<this.myProjects.length;i++)
        {
          this.myProjects[i].Display = true
        }
      },

      addProject: function () {
        this.setProjectCreateDialogShow(true)
      }

    },
    created: function () {
       this.loadMyProject()
    },
    components: {},
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import '../../components/layout/appBody';
@import '../../components/layout/appHead';
@import '../../assets/teamcat/global/less/global';
.project-search-item{
  padding: 4px 0;
  border-bottom: 1px solid #F6F6F6;
  height:40px;
}

.project-search-item-title{
  color:inherit;
  padding-left: 20px;
}

</style>
