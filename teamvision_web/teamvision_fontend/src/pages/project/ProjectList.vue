<template>
  <div class="layout-content portal-list-container" :style="'height:'+ projectContainerHeight +'px;'+' overflow-y: scroll'">
        <Card   v-for="project in myProjectList" v-if="project.Display" :key="project.id" style=" width:230px;height:180px;float:left;margin:20px;" :bordered="false">
          <div style="text-align:center;height:110px;">
            <a :href="'/project/'+ project.id +'/issue/all'">
              <img :src="'' + project.PBAvatar" class="project_icon">
            </a>
          </div>
          <div><div style="padding-top: 10px;color:#333;text-align: center">{{ project.PBTitle }}</div></div>
        </Card>
        <project-create-dialog></project-create-dialog>
  </div>
</template>

<script>
  import store from '../../store/index.js'
  import { mapGetters,mapMutations} from 'vuex'
  import ProjectCreateDialog from './ProjectCreateDialog.vue'

  export default {
    name: 'projectList',
    data () {
      return {
        myProject:[]
      }
    },
    computed: {
      ...mapGetters(['appBodyHeight']),
      ...mapGetters('project',['projectSearchKey','projectAdded']),
      projectContainerHeight: function () {
        return this.appBodyHeight
      },
      myProjectList: function () {
        if(this.projectSearchKey === '')
        {
           this.initProjectDisplayStatus()
        }
        else{
           this.filterProjectList(this.projectSearchKey)
        }

        if(this.projectAdded)
        {
          this.loadProjectList()
          this.setProjectAdded(false)
        }
        return this.myProject
      }
    },
    methods: {
      ...mapMutations('project', ['setProjectAdded']),

      filterProjectList: function (value) {
        this.initProjectDisplayStatus()
        for(let i=0; i<this.myProject.length;i++)
        {
          let temp = this.myProject[i]
          if(temp.PBTitle.toUpperCase().indexOf(value.toUpperCase())<0)
          {
            temp.Display = false
          }
        }
      },
      initProjectDisplayStatus: function () {
        for(let i=0; i<this.myProject.length;i++)
        {
          this.myProject[i].Display = true
        }
      },

      loadProjectList: function () {
        this.$axios.get('/api/project/list?extinfo=0&my=1').then(response => {
          this.myProject = response.data.result
        }, response => {
          this.setTaskChange(true)

        })
      }
    },
    created: function () {
     this.loadProjectList()

    },
    components: {ProjectCreateDialog}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  @import "../../../src/assets/teamcat/global/less/common_controlls";

  .project_icon
  {
    width:80%;
    height:80px;
  }
</style>
