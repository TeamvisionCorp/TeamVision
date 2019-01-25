<template>
  <Modal :value="ciTaskCreateDialogShow" title="添加新任务" :width="600" @on-cancel="cancel"   :styles="{bottom:'20px',top: '50px'}">
    <div :style="'height:' + containerHeight + 'px;overflow-y: scroll;overflow-x: hidden'">
      <Form  ref="ciTaskCreate" :model="formItem" :label-width="80" :rules="ruleCustom">
        <FormItem label="项目" prop="Project">
          <Select v-model="formItem.Project"  placeholder="请选择项目" @on-change="onProjectChange">
            <Option v-for="project in projects" :key="project.id" :value="project.id" :label="project.PBTitle">
              <span style="margin-right: 10px;" ><Avatar :src="project.PBAvatar" /></span>
              <span >{{ project.PBTitle }}</span>
            </Option>
          </Select>
        </FormItem>
        <FormItem label="标题" prop="TaskName">
          <Input v-model="formItem.TaskName" placeholder="任务名称50个字符以内！" />
        </FormItem>
        <FormItem label="构建记录保留个数" prop="HistoryCleanStrategy">
          <Input v-model="formItem.HistoryCleanStrategy" placeholder="默认10个"/>
        </FormItem>
        <FormItem label="任务类型" prop="TaskType">
          <Select v-model="formItem.TaskType" :filterable="true" placeholder="任务类型" @on-change="onTaskTypeChange">
            <Option  :key="0" :value="0">复制任务</Option>
            <Option  :key="4" :value="4">构建</Option>
            <Option :key="1" :value="1">测试</Option>
            <Option  :key="5" :value="5">部署</Option>
          </Select>
        </FormItem>
        <FormItem label="任务列表" v-if="showTaskList" prop="CopyTaskID">
          <Select v-model="formItem.CopyTaskID" :filterable="true" placeholder="复制任务列表">
            <Option v-for="task in ciTaskList" :key="task.id" :value="task.id">{{ task.TaskName }}</Option>
          </Select>
        </FormItem>
      </Form>
    </div>
    <div slot="footer">
      <Button v-if="ciTaskCreateDialogShow" type="success"  style="width: 80px; height:30px;" shape="circle" @click="addCITask('ciTaskCreate')">添加</Button>
      <!--<Button type="ghost"  style="width: 80px; height:30px;"  shape="circle" @click="cancel">取消</Button>-->
    </div>
</Modal>
</template>

<script>
import { mapGetters,mapMutations } from 'vuex'
import { ciTaskValidateRules } from './CITaskCreateDialog'
import FormItem from '../../../../node_modules/iview/src/components/form/form-item.vue'

  export default {
    name: 'CITaskCreateDialog',
    data () {
      return {
        projects: [],
        ciTaskList: [],
        showTaskList: true,
        formItem: {
          CopyTaskID: 0,
          TaskName: '',
          Project: 0,
          TaskType: 0,
          HistoryCleanStrategy: 10
        },
        ruleCustom: {
          ...ciTaskValidateRules
        }
      }

    },
    computed: {
      ...mapGetters('citask',['ciTaskCreateDialogShow']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight-100
      },
    },
    methods:
      {
        ...mapMutations('citask',['setCITaskCreateDialogShow','setCITaskAdded']),

        addCITask (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {
              this.$axios.post('/api/ci/task_basic/list', this.formItem).then(response => {
                this.setCITaskCreateDialogShow(false)
                this.setCITaskAdded(true)
              }, response => {
                this.setCITaskCreateDialogShow(false)
                this.$Message.error({
                  content: '创建任务失败，请联系管理员或者重试',
                  duration: 10
                })
              })

            }
          })
        },
        cancel () {
          this.setCITaskCreateDialogShow(false)
        },

        onTaskTypeChange: function (value) {
          if ( value ===0 )
          {
            this.showTaskList = true
          }
          else
          {
            this.showTaskList = false
          }

        },

        onProjectChange: function () {
          console.log(this.formItem)
        },

        loadMyProject: function () {
          this.$axios.get('/api/project/list?extinfo=1&home=1').then(response => {
            this.projects=response.data.result
          }, response => {
            // error callback
          })
        },

        loadMyCITasks: function () {
          this.$axios.get('/api/ci/task_basic/my?page_size=10000').then(response => {
            this.ciTaskList=response.data.result.results
          }, response => {
            // error callback
          })
        }

      },
    created () {
      this.loadMyProject()
      this.loadMyCITasks()
    },
    mounted () {

    },
    watch: {

    },
    components: {
      FormItem
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
