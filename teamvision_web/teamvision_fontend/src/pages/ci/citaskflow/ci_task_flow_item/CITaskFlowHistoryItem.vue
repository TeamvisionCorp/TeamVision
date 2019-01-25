<template>
  <Scroll :on-reach-bottom="handleReachBottom" :height="historyContainerHeight">
    <Collapse simple accordion @on-change="changeHistory">
      <Panel :name="''+flowHistory.id" :key="flowHistory.id" style="padding-bottom:12px;"
             v-for="flowHistory in taskFlowHistories.results" v>
      <span style="padding-right: 5px;">
        <Tooltip content="执行中">
          <Icon v-if="flowHistory.Status ===0" type="ios-remove-circle" style="color:#337ab7;"></Icon>
        </Tooltip>
        <Tooltip content="成功">
          <Icon v-if="flowHistory.Status ===1" type="ios-checkmark-circle" style="color:#388e83;"></Icon>
        </Tooltip>
        <Tooltip content="失败">
          <Icon v-if="flowHistory.Status ===2" type="ios-close-circle" style="color:darkred"></Icon>
        </Tooltip>
      </span>
        <span style="padding-right: 20px;">#{{ flowHistory.id }}</span>
        <span style="padding-right: 20px; min-width:200px;display: inline-block;  ">{{ flowHistory.StartTimeFormat }}
          </span>
        <span style="padding-right: 20px;"><Avatar style="background-color:#388e83" size="small">{{ flowHistory.StartedUser }}</Avatar></span>
        <div slot="content" v-if="flowHistory.Status!==0">
          <div
            :style="'height:'+historyContainerHeight-78+'px'+'; overflow-y:scroll;padding-right:10px;'">
            <flow-section v-for="sectionHistory in flowHistory.SectionHistories" :key="sectionHistory.id"
                          :columnID="sectionHistory.id" group="flowHistory"
                          v-bind:itemList.sync="sectionHistory.TaskHistories" :columnTitle="sectionHistory.SectionName"
                          :dishover="false" :shadow="false" :bordered="true"
                          @end="onEnd"
                          style="margin-left: 10px;">
              <Card slot='column-header' :bordered="false" :shadow="false" :dis-hover="true" class="board-column-title">
               <span>
                 <Avatar size="small" style="border: 1px solid black;background-color: #f5f7f9;color: #5f5f5f;margin-right: 0px;">{{ sectionHistory.SectionIndex}}</Avatar>
                     <span style="font-size: 16px;">{{ sectionHistory.SectionName }}</span>
                  <Tooltip content="执行中">
          <Icon v-if="sectionHistory.Status ===0" type="ios-remove-circle" style="color:#337ab7;"></Icon>
        </Tooltip>
        <Tooltip content="成功">
          <Icon v-if="sectionHistory.Status ===1" type="ios-checkmark-circle" style="color:#388e83;"></Icon>
        </Tooltip>
        <Tooltip content="失败">
          <Icon v-if="sectionHistory.Status ===2" type="ios-close-circle" style="color:darkred"></Icon>
        </Tooltip>
               </span>
              </Card>
              <template slot-scope="slotProps">
                <ci-task-history-item :item="slotProps.element"></ci-task-history-item>
              </template>
            </flow-section>
          </div>
        </div>
      </Panel>
    </Collapse>
  </Scroll>
</template>

<script>
  import store from '../../../../store/index.js'
  import { mapGetters, mapMutations } from 'vuex'
  import SectionCreateDialog from './CISectionAddDialog.vue'
  import TaskAddToSectionDialog from './SectionTaskAddDialog.vue'
  import ciTaskHistoryItem from '../../citask/CITaskHistoryItem.vue'
  import FlowSection from './CITaskFlowSection.vue'

  export default {
    name: 'flowHistoryItem',
    props: ['flowID'],
    data () {
      return {
        taskFlowHistories: {},
        currentSection: 0,
      }
    },
    computed: {
      ...mapGetters('citaskflow', ['addedSection', 'ciTaskAddedToSection', 'sectionRenamed']),
      ...mapGetters(['appBodyHeight']),
      historyContainerHeight: function () {
        return this.appBodyHeight - 38
      },
      taskFlowID: function () {
        if (this.flowID + '' === 'undefined') {
          return 0
        }
        else {
          return this.flowID
        }

      },
      sectionID: function () {
        return this.currentSection
      }

    },
    methods: {
      ...mapMutations('citaskflow', ['setAddedSection', 'setAddedSectionDialogShow', 'setSectionRenamed', 'setRenameSectionDialogShow', 'setCITaskAddedToSectionDialogShow', 'setCITaskAddedToSection']),
      loadFlowHistory: function (flowID) {
        if (flowID + '' !== '0') {
          this.$axios.get('/api/ci/task_flow/' + this.flowID + '/history/list?page_size=17').then(response => {
            this.taskFlowHistories = response.data.result
          }, response => {
          })
        }
      },

      editSection: function (sectionID) {
        this.currentSection = sectionID
        this.setCITaskAddedToSectionDialogShow(true)
      },

      handleReachBottom () {
        if (this.taskFlowHistories.next !== null) {
          this.$axios.get(this.taskFlowHistories.next).then(response => {
            this.taskFlowHistories.results.push(...response.data.result.results)
            this.taskFlowHistories.next = response.data.result.next
          }, response => {
          })
        }
      },

      onEnd (evt) {
        let toID = evt.to.getAttribute('id')
        let fromID = evt.from.getAttribute('id')
        let itemOldIndex = evt.oldIndex
        let itemNewIndex = evt.newIndex
        let itemID = evt.item.getAttribute('id')
        this.alterColumnData(fromID, toID, itemID, itemOldIndex, itemNewIndex)
        this.$axios.patch('/api/project/task/' + itemID + '/', {'Status': toID}).then(response => {
          console.log(response)
        }, response => {
          this.setTaskChange(true)

        })

      },

      flowContextMenuClick: function (itemCommand) {
        let commandArray = itemCommand.split(':')
        let command = commandArray[0]
        let commandParameter = commandArray[1]
        this.currentSection = commandParameter
        if (command === 'rename') {
          this.setRenameSectionDialogShow(true)
        }

        if (command === 'start') {
          this.startSection(commandParameter)
        }

        if (command === 'delete') {
          let sectionName = this.findSection(commandParameter).SectionName
          this.$Modal.confirm({
            title: '删除确认',
            content: '<p>删除是危险操作，确认要删除任务阶段 [' + sectionName + ' ] 吗？</p>',
            onOk: () => {
              this.deleteFlowSection(commandParameter)
            },
            onCancel: () => {
            }
          })

        }
      },

      deleteFlowSection: function (sectionid) {
        this.$axios.delete('/api/ci/task_flow/section/' + sectionid).then(response => {
          this.loadFlowTasks(this.taskFlowID)
        }, response => {
          // error callback
        })
      },

      startSection: function (sectionid) {
        this.$axios.get('/api/ci/flow_section/' + sectionid + '/start/').then(response => {
          this.$Message.success({
            content: response.data.result.message,
            duration: 10
          })
        }, response => {
          // error callback
        })
      },

      findSection: function (sectionID) {
        let result = null
        for (let i = 0; i < this.taskFlow.Sections.length; i++) {
          if (this.taskFlow.Sections[i].id + '' === sectionID) {
            result = this.taskFlow.Sections[i]
            break
          }
        }
        return result
      },

      changeHistory: function (value) {
        console.log(value)
      }
    },

    created: function () {
      this.loadFlowHistory(this.taskFlowID)
    },

    watch: {

      taskFlowID: function () {
        this.loadFlowHistory(this.taskFlowID)
      }
    },

    components: {
      SectionCreateDialog,
      ciTaskHistoryItem,
      FlowSection,
      TaskAddToSectionDialog
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

  .task-flow-title {
    height: 80px;
    width: 80px;
    line-height: 80px;
    display: inline-block;
    color: #5e5e5e;
    text-align: center;
  }

  .board-column-title {
    background: #f5f7f9;
    margin-top: -15px;
    text-align: center;
  }
</style>
