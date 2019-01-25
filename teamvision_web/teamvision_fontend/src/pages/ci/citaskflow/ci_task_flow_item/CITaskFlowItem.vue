<template>
  <div :style="'height:'+taskContainerHeight+'px'+'; overflow-y:scroll;padding-left:10px;padding-right:10px;'">
    <flow-section v-for="section in taskFlow.Sections" :key="section.id" :columnID="section.id" :group="taskFlowID"
                  v-bind:itemList.sync="section.Tasks" :columnTitle="section.SectionName" :dishover="false" :shadow="false" :bordered="true"
                  style="border-top:none;border-bottom: none;border-right: none" @end="onEnd" @reachBottom="onReachBottom">
      <Card  slot='column-header' :bordered="false" :shadow="false" :dis-hover="true" class="board-column-title">
        <span><Avatar size="small" style="border: 1px solid black;background-color: #f5f7f9;color: #5f5f5f;margin-right: 10px;">{{ section.SectionIndex }}</Avatar>  <span style="font-size: 16px;">{{ section.SectionName }}</span>
        </span>
        <span class="pull-left cursor-hand" @click="editSection(section.id)" >
          <Icon v-if="section.Tasks.length<1" type="md-add" :size="16" color="#388e83" />
          <Icon v-if="section.Tasks.length>0" type="ios-create-outline" :size="16" color="#388e83"/>
        </span>
        <span class="pull-right cursor-hand" style="color:#5f5f5f;margin-right: -6px;">
          <Dropdown @on-click="flowContextMenuClick">
        <i class="fa fa-bars fa-fw"></i>
        <DropdownMenu slot="list">
            <DropdownItem :name="'start:'+section.id" style="height: 20px;padding-top: 2px;text-align: left">
              <span style="margin-right: 5px;">
                <Icon type="md-play"></Icon>
              </span>
              <span>执行</span>
            </DropdownItem>
            <DropdownItem :name="'rename:'+section.id" style="height: 20px;padding-top: 2px;text-align: left">
              <span style="margin-right: 5px;">
                <Icon type="md-create"></Icon>
              </span>
              <span>重命名</span>
            </DropdownItem>
             <DropdownItem :name="'delete:'+section.id" style="height: 20px;padding-top: 2px; text-align: left">
              <span style="margin-right: 5px;">
                <Icon type="ios-trash"></Icon>
              </span>

              <span>删除</span>
            </DropdownItem>
        </DropdownMenu>
    </Dropdown>
        </span>
      </Card>
      <template slot-scope="slotProps">
        <ci-task-item :item="slotProps.element"></ci-task-item>
      </template>
    </flow-section>
    <section-create-dialog :flowID="taskFlowID" :sectionID="sectionID"></section-create-dialog>
    <task-add-to-section-dialog :sectionID="sectionID" ></task-add-to-section-dialog>
  </div>
</template>

<script>
  import store from '../../../../store/index.js'
  import { mapGetters, mapMutations} from 'vuex'
  import SectionCreateDialog from './CISectionAddDialog.vue'
  import TaskAddToSectionDialog from './SectionTaskAddDialog.vue'
  import ciTaskItem from '../../citask/CITaskItem.vue'
  import FlowSection from './CITaskFlowSection.vue'
  export default {
    name: 'ciTaskFlowItem',
    props: ['flowID'],
    data () {
      return {
         taskFlow: {
         },
        currentSection: 0,
      }
    },
    computed: {
        ...mapGetters('citaskflow', ['addedSection','ciTaskAddedToSection','sectionRenamed']),
      ...mapGetters(['appBodyHeight']),
      taskContainerHeight: function () {
        return  this.appBodyHeight
      },
      taskFlowID: function () {
        if(this.flowID+'' === 'undefined')
        {
          return 0
        }
        else
        {
          return this.flowID
        }

      },
      sectionID: function () {
        return this.currentSection
      }

    },
    methods: {
      ...mapMutations('citaskflow', ['setAddedSection','setAddedSectionDialogShow','setSectionRenamed','setRenameSectionDialogShow','setCITaskAddedToSectionDialogShow','setCITaskAddedToSection']),
      loadFlowTasks: function (flowID) {
        if(flowID+'' !=='0') {
          this.$axios.get('/api/ci/task_flow/' + flowID + '/').then(response => {
            this.taskFlow = response.data.result
          }, response => {
          })
        }
      },

      editSection: function (sectionID) {
        this.currentSection = sectionID
        this.setCITaskAddedToSectionDialogShow(true)
      },

      onReachBottom (columnid) {
      },

      onEnd (evt) {
        console.log(evt)
        let toID = evt.to.getAttribute('id')
        let fromID = evt.from.getAttribute('id')
        let itemID = evt.item.getAttribute('id')
        let itemOldIndex = evt.oldIndex
//        let itemNewIndex = evt.newIndex
        let toSection = this.findSection(toID)
        let fromSection = this.findSection(fromID)
        toSection.CITaskIDs.push(itemID)
        fromSection.CITaskIDs.splice(itemOldIndex,1)
        console.log(toSection)
        console.log(fromSection)
        this.$axios.patch('/api/ci/task_flow/section/'+toID,{'CITasks': toSection.CITaskIDs.toString()}).then(response => {
          console.log(response)
        }, response => {
        })

        this.$axios.patch('/api/ci/task_flow/section/'+fromID,{'CITasks': fromSection.CITaskIDs.toString()}).then(response => {
          console.log(response)
        }, response => {
        })

      },

      flowContextMenuClick: function (itemCommand) {
        let commandArray = itemCommand.split(':')
        let command = commandArray[0]
        let commandParameter = commandArray[1]
        this.currentSection = commandParameter
        if(command === 'rename')
        {
          this.setRenameSectionDialogShow(true)
        }

        if(command === 'start')
        {
          this.startSection(commandParameter)
        }

        if(command === 'delete')
        {
          let sectionName = this.findSection(commandParameter).SectionName
          this.$Modal.confirm({
            title: '删除确认',
            content: '<p>删除是危险操作，确认要删除任务阶段 ['+sectionName+' ] 吗？</p>',
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
        this.$axios.get('/api/ci/flow_section/' + sectionid+'/start/').then(response => {
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
        for(let i=0;i<this.taskFlow.Sections.length; i++)
        {
          if(this.taskFlow.Sections[i].id+''=== sectionID)
          {
            result = this.taskFlow.Sections[i]
            break
          }
        }
        return result
      },

    },

    created: function () {
      this.loadFlowTasks(this.taskFlowID)
    },

    watch: {
      addedSection: function (value) {
        if (value)
        {
          this.loadFlowTasks(this.taskFlowID)
          this.setAddedSection(false)
        }
      },

      sectionRenamed: function (value) {
        if (value)
        {
          this.loadFlowTasks(this.taskFlowID)
          this.setSectionRenamed(false)
        }
      },

      ciTaskAddedToSection: function (value) {
     if (value)
      {
         this.loadFlowTasks(this.taskFlowID)
        this.setCITaskAddedToSection(false)
      }
     },

      taskFlowID: function () {
        this.loadFlowTasks(this.taskFlowID)
      }
    },

    components: {
      SectionCreateDialog,
      ciTaskItem,
      FlowSection,
      TaskAddToSectionDialog
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .env_archive_folder
  {
    border:1px solid #f0f0f0;
    width:250px;
    height:150px;
    margin:10px 10px 10px 30px;
    border-radius:5px;
    cursor:pointer;
    float: left;
    padding:0px;
  }

  .env_archive_folder_header
  {
    height:0px;
  }

  .env_archive_folder_body
  {
    height:90px;
  }

  .env_archive_folder_body center
  {
    padding-top: 10px;
    color:#d3d7d4;
  }

  .env_archive_folder_footer
  {
    border-top:1px solid #f0f0f0;
    height:50px;
  }

  .env_archive_folder_version
  {
    padding:10px 5px 5px 5px;
    font-size: 14px;
    color: black;
    overflow:hidden;

  }

  .env_archive_version_file
  {
    padding:5px 5px 0px 5px;
    font-size: 14px;
    color: black;
    overflow:hidden;

  }

  .task-flow-title{
    height: 80px;
    width: 80px;
    line-height: 80px;
    display:inline-block;
    color: #5e5e5e;
    text-align:center;
  }

  .board-column-title{
    background: #f5f7f9;
    margin-top:-15px;
    text-align: center;
  }
</style>
