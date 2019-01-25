<template>
  <div>
      <ci-task-item  v-for="task in myCITaskList.items" :key="task.id" :item="task"></ci-task-item>
  </div>
</template>

<script>
  import store from '../../../store/index.js'
  import { mapGetters,mapMutations} from 'vuex'
  import ciTaskItem from './CITaskItem.vue'
  export default {
    name: 'ciTask',
    data () {
      return {
        myCITask: {
          count: 0,
          next: '',
          items: []
        }
      }
    },
    computed: {
      ...mapGetters('citask',['ciTaskSearchKey','ciTaskAdded']),
      ciTaskCount: function () {
        return this.myCITask.count
      },
      myCITaskList: function () {
         if(this.ciTaskSearchKey==='')
         {
           this.initCITaskStatus()
         }
         else
         {
           this.filterCITask(this.ciTaskSearchKey)
         }
         if(this.ciTaskAdded)
         {
           this.loadCITaskList()
           this.setCITaskAdded(false)
         }
         return this.myCITask
      }
    },
    methods: {
      ...mapMutations('citask',['setCITaskAdded']),
      loadCITaskList: function () {
        this.$axios.get('/api/ci/task_basic/my?page_size=100').then(response => {
          this.myCITask.count = response.data.result.count
          this.myCITask.next = response.data.result.next
          this.myCITask.items = response.data.result.results
          this.$Spin.hide()
        }, response => {
          this.$Spin.hide()
        })
      },
      filterCITask: function (key) {
        this.initCITaskStatus()
        for(let i=0;i<this.myCITask.items.length;i++)
        {
           let temp = this.myCITask.items[i]
           if(temp.TaskName.toUpperCase().indexOf(key.toUpperCase())<0)
           {
             temp.Display = false
             this.myCITask.count--
           }
        }

      },
      initCITaskStatus: function () {
        this.myCITask.count = this.myCITask.items.length
        for(let i=0;i<this.myCITask.items.length;i++)
        {
          let temp = this.myCITask.items[i]
          temp.Display = true
        }
      },
    },
    mounted: function () {
      if (this.ciTaskCount === 0) {
        this.$Spin.show()
      }
    },
    created: function () {
     this.loadCITaskList()
    },
    watch: {
      ciTaskCount: function () {
        if (this.ciTaskCount !== 0) {
          this.$Spin.hide()
        }
      }
    },
    components: {
      ciTaskItem
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
