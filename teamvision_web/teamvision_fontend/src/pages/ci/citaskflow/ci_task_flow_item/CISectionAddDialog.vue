<template>
  <Modal :value="showDialog" :title="dialogTitle" :width="600"  @on-cancel="cancel"   :styles="{bottom:'20px',top: '50px'}">
    <div style="height:100px;overflow-y: scroll;overflow-x: hidden">
      <Form  ref="ciSectionCreate" :model="formItem" :label-width="80" :rules="ruleCustom" :id="taskFlowID">
        <FormItem label="阶段名称"  prop="SectionName">
          <Input v-model="formItem.SectionName" placeholder="阶段名称50个字符以内！" />
        </FormItem>
      </Form>
    </div>
    <div slot="footer">
      <Button  type="success"  style="width: 80px; height:30px;" shape="circle" @click="addSection('ciSectionCreate')">确定</Button>
    </div>
</Modal>
</template>

<script>
import { mapGetters,mapMutations } from 'vuex'
import FormItem from '../../../../../node_modules/iview/src/components/form/form-item.vue'

  export default {
    name: 'TaskFlowSectionCreateDialog',
    props: ['flowID','sectionID'],
    data () {
      return {
        currentFlow: {},
        formItem: {
          SectionName: '',
          TaskFlow: 0,
          SectionOrder: 0
        },
        ruleCustom: {
          SectionName: [
            { type: 'string', required: true, min: 1, max: 50, message: '阶段名称长度必须在1-50个字符之间！', trigger: 'blur' }
          ],
        }
      }

    },
    computed: {
      ...mapGetters('citaskflow',['addedSectionDialogShow','renameSectionDialogShow']),
      taskFlowID: function () {
        if(this.flowID+'' ==='undefined')
        {
          return 0
        }
        else
        {
          return this.flowID
        }
      },
      showDialog: function () {
        return this.renameSectionDialogShow || this.addedSectionDialogShow
      },

      dialogTitle: function () {
        if(this.addedSectionDialogShow)
        {
          return '添加阶段'
        }

        if(this.renameSectionDialogShow)
        {
          return '重命名阶段'
        }
      }

    },
    methods:
      {
        ...mapMutations('citaskflow',['setAddedSectionDialogShow', 'setAddedSection','setRenameSectionDialogShow','setSectionRenamed']),
        addSection (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {
              if (this.addedSectionDialogShow)
              {
                this.formItem.SectionOrder = this.currentFlow.MaxOrder+1
                this.formItem.TaskFlow = this.currentFlow.id
                this.$axios.post('/api/ci/task_flow/'+this.taskFlowID+'/sections', this.formItem).then(response => {
                  this.setAddedSection(true)
                  this.setAddedSectionDialogShow(false)
                }, response => {
                  this.setAddedSectionDialogShow(false)
                  this.$Message.error({
                    content: '创建工作流阶段失败，请联系管理员或者重试',
                    duration: 10
                  })
                })
              }
              if (this.renameSectionDialogShow)
              {
                this.$axios.patch('/api/ci/task_flow/section/'+this.sectionID,{SectionName:this.formItem.SectionName}).then(response => {
                  this.setSectionRenamed(true)
                  this.setRenameSectionDialogShow(false)
                }, response => {
                  this.setRenameSectionDialogShow(false)
                  this.$Message.error({
                    content: '重命名工作流阶段失败，请联系管理员或者重试',
                    duration: 10
                  })
                })
              }
            }
          })
        },

        cancel () {
          this.setAddedSectionDialogShow(false)
          this.setRenameSectionDialogShow(false)
        },

        loadFlowTasks: function (flowID) {
          if(flowID+'' !=='0') {
            this.$axios.get('/api/ci/task_flow/' + flowID + '/').then(response => {
              this.currentFlow = response.data.result
            }, response => {
            })
          }
        },

        loadMyCITasks: function () {
          this.$axios.get('/api/ci/task_basic/my?page_size=10000').then(response => {
            let ciTaskList = response.data.result.results

          }, response => {
            // error callback
          })
        },

        loadSection: function (sectionID) {
          if(sectionID+'' !=='0') {
            this.$axios.get('/api/ci/task_flow/section/' + sectionID).then(response => {
              this.formItem.SectionName = response.data.result.SectionName
            }, response => {
            })
          }
        },

      },
    created () {
      this.loadMyCITasks()
      this.loadFlowTasks(this.taskFlowID)
    },
    mounted () {

    },
    watch: {
      flowID: function (value) {
        this.loadFlowTasks(this.taskFlowID)
      },
      sectionID: function () {
        this.loadSection(this.sectionID)

      }
    },
    components: {
      FormItem
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">


</style>
