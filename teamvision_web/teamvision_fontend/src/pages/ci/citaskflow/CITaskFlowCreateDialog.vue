<template>
  <Modal :value="ciTaskFlowCreateDialogShow" title="添加新任务流" :width="600"  @on-cancel="cancel"   :styles="{bottom:'20px',top: '50px'}">
    <div :style="'height:' + containerHeight + 'px;overflow-y: scroll;overflow-x: hidden'">
      <Form  ref="ciTaskFlowCreate" :model="formItem" :label-width="80" :rules="ruleCustom">
        <FormItem label="项目" prop="Project">
          <Select v-model="formItem.Project" :filterable="true" placeholder="请选择项目">
            <Option v-for="project in projects" :key="project.id" :value="project.id" :label="project.PBTitle">
              <span style="margin-right: 10px;" ><Avatar :src="project.PBAvatar" /></span>
              <span >{{ project.PBTitle }}</span>
            </Option>
          </Select>
        </FormItem>
        <FormItem label="标题" prop="FlowName">
          <Input v-model="formItem.FlowName" placeholder="任务流名称50个字符以内！" />
        </FormItem>

        <!--<FormItem label="描述" prop="Description">-->
          <!--<Input v-model="formItem.Description" type="textarea" :rows="4" placeholder="200个字以内的描述！" />-->
        <!--</FormItem>-->

        <FormItem label="添加任务"  prop="FlowTaskList">
          <Transfer :data="ciTaskTransfer.ciTasks" :target-keys="ciTaskTransfer.targetKeys" :render-format="transferRender" :filterable="true" :filter-method="transferFilterMethod"
            @on-change="moveCITasks" :titles="ciTaskTransfer.titles" :list-style="ciTaskTransfer.listStyle"></Transfer>
        </FormItem>
      </Form>
    </div>
    <div slot="footer">
      <Button v-if="ciTaskFlowCreateDialogShow" type="success"  style="width: 80px; height:30px;" shape="circle" @click="addCITaskFlow('ciTaskFlowCreate')">添加</Button>
    </div>
</Modal>
</template>

<script>
import { mapGetters,mapMutations } from 'vuex'
import { ciTaskFlowValidateRules } from './CITaskFlowCreateDialog'
import FormItem from '../../../../node_modules/iview/src/components/form/form-item.vue'

  export default {
    name: 'CITaskFlowCreateDialog',
    data () {
      return {
        projects: [],
        ciTaskTransfer: {
          ciTasks: [],
          targetKeys: [],
          titles: ['我的任务', '添加的任务'],
          listStyle: {
            height: '249px'
          }
        },
        formItem: {
          FlowName: '',
          Project: 0,
//          Description: '工作流描述',
          CITasks: []
        },
        ruleCustom: {
          ...ciTaskFlowValidateRules
        }
      }

    },
    computed: {
      ...mapGetters('citaskflow',['ciTaskFlowCreateDialogShow']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight-100
      },
    },
    methods:
      {
        ...mapMutations('citaskflow',['setCITaskFlowCreateDialogShow', 'setCITaskFlowAdded']),
        addCITaskFlow (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {

              this.$axios.post('/api/ci/task_flow/list', this.formItem).then(response => {
                this.setCITaskFlowCreateDialogShow(false)
                this.setCITaskFlowAdded(true)
              }, response => {
                this.setCITaskFlowCreateDialogShow(false)
                this.$Message.error({
                  content: '创建任务流失败，请联系管理员或者重试',
                  duration: 10
                })
              })

            }
          })
        },
        cancel () {
          this.setCITaskFlowCreateDialogShow(false)
        },
        transferRender: function (item) {
          return item.label
        },
        moveCITasks (newTargetKeys) {
          this.ciTaskTransfer.targetKeys = newTargetKeys
          this.formItem.CITasks = newTargetKeys
          console.log(this.formItem)
        },
        transferFilterMethod (data, query) {
          return data.label.toUpperCase().indexOf(query.toUpperCase()) > -1
        },
        loadMyCITasks: function () {
          this.$axios.get('/api/ci/task_basic/my?page_size=10000').then(response => {
            let ciTaskList = response.data.result.results
            for (let i = 0; i < ciTaskList.length; i++)
            {
              this.ciTaskTransfer.ciTasks.push({
                key: ciTaskList[i].id,
                label: ciTaskList[i].TaskName,
                description: ciTaskList[i].Description
              })
            }

          }, response => {
            // error callback
          })
        },
        loadFlowCITasks: function () {

        },

        loadMyProject: function () {
          this.$axios.get('/api/project/list?extinfo=1&home=1').then(response => {
            this.projects=response.data.result
          }, response => {
            // error callback
          })
        },

      },
    created: function () {
      this.loadMyCITasks()
      this.loadFlowCITasks()
      this.loadMyProject()
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
