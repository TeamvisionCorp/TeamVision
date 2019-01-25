<template>
  <Modal :value="ciTaskAddedToSectionDialogShow" title="添加任务" :width="600" @on-ok="addCITaskToSection" @on-cancel="cancel"   :styles="{bottom:'20px',top: '50px'}">
    <div style="height:300px;overflow-y: scroll;overflow-x: hidden">
      <Form  ref="ciTaskAddToSectionCreate" :model="formItem" :label-width="80" :rules="ruleCustom" :id="sectionID">
        <FormItem label=""  prop="FlowTaskList">
          <Transfer :data="ciTaskTransfer.ciTasks" :target-keys="ciTaskTransfer.targetKeys" :render-format="transferRender" :filterable="true" :filter-method="transferFilterMethod"
                    @on-change="moveCITasks" :titles="ciTaskTransfer.titles" :list-style="ciTaskTransfer.listStyle"></Transfer>
        </FormItem>
      </Form>
    </div>
    <div slot="footer">
      <Button v-if="ciTaskAddedToSectionDialogShow" type="success"  style="width: 80px; height:30px;" shape="circle" @click="addCITaskToSection">确定</Button>
    </div>
  </Modal>
</template>

<script>
  import { mapGetters,mapMutations } from 'vuex'
  import FormItem from '../../../../../node_modules/iview/src/components/form/form-item.vue'

  export default {
    name: 'TaskAddToSectionDialog',
    props: ['sectionID'],
    data () {
      return {
        projects: [],
        ciTaskTransfer: {
          ciTasks: [],
          targetKeys: [0],
          titles: ['可添加任务', '已添加的任务'],
          listStyle: {
            height: '249px'
          }
        },
        formItem: {},
        ruleCustom: {
        }
      }

    },
    computed: {
      ...mapGetters('citaskflow',['ciTaskAddedToSectionDialogShow'])
    },
    methods:
      {
        ...mapMutations('citaskflow',['setCITaskAddedToSectionDialogShow', 'setCITaskAddedToSection']),
        addCITaskToSection () {
          let targetTasks = ''
          for (let i = 0; i < this.ciTaskTransfer.targetKeys.length; i++) {
            if (this.ciTaskTransfer.targetKeys[i]) {
              targetTasks = targetTasks + this.ciTaskTransfer.targetKeys[i] + ','
            }
          }
//          if (targetTasks !== '')
//          {
            this.$axios.patch('/api/ci/task_flow/section/' + this.sectionID, {'CITasks': targetTasks}).then(response => {
              this.setCITaskAddedToSectionDialogShow(false)
              this.setCITaskAddedToSection(true)
            }, response => {
              this.setCITaskAddedToSectionDialogShow(false)
              this.$Message.error({
                content: '添加任务失败，请联系管理员或者重试',
                duration: 10
              })
            })
//          }
        },

        cancel () {
          this.setCITaskAddedToSectionDialogShow(false)
        },

        transferRender: function (item) {
          return item.label
        },

        moveCITasks (newTargetKeys, direction, moveKeys) {
          if(newTargetKeys.length !== 0)
          {
            this.ciTaskTransfer.targetKeys = newTargetKeys
          }
          else
          {
            this.ciTaskTransfer.targetKeys =[0]
          }
        },

        transferFilterMethod (data, query) {
          return data.label.toUpperCase().indexOf(query.toUpperCase()) > -1
        },

        loadSectionTasks: function (sectionID) {
          console.log(sectionID)
          if(sectionID+'' !=='0') {
            this.$axios.get('/api/ci/task_flow/section/' + sectionID).then(response => {
              let currentSection = response.data.result
                let flowTasks = currentSection.CITasks.replace('[', '').replace(']', '').split(',')
                this.ciTaskTransfer.targetKeys = []
                for (let i = 0; i < flowTasks.length; i++) {
                  this.ciTaskTransfer.targetKeys.push(parseInt(flowTasks[i].trim()))
                }
            }, response => {
            })
          }
          else {
            this.ciTaskTransfer.targetKeys = []
          }
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
        }

      },
    created () {
      this.loadMyCITasks()
      this.loadSectionTasks(this.sectionID)
    },
    mounted () {

    },
    watch: {
      sectionID: function () {
        this.loadSectionTasks(this.sectionID)
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

