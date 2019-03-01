<template>
  <div>
    <gantt-data-source ref="ganttdatasource1"
                           :transport-read-url="getTaskUrl"
                           transport-read-data-type="json"
                           transport-update-url="/api/project/task/update/"
                           transport-update-data-type="json"
                           transport-update-type="PUT"
                           transport-create-url="/api/project/task/create/"
                           transport-create-data-type="json"
                           transport-create-type="POST"
                           transport-destroy-url="/api/project/task/delete/"
                           transport-destroy-data-type="json"
                           transport-destroy-type="DELETE"
                           :transport-parameter-map="parameterMap"
                           schema-model-id="id"
                           :schema-model-fields="fields"
                           :schema-data="taskResultData"
                       :resources="resources"
                       :assignments="assignments">
    </gantt-data-source>

    <gantt-dependency-data-source ref="ganttdependencydatasource1"
                                     transport-read-url="/api/project/task_dependencies"
                                     transport-read-data-type="json"
                                     transport-update-url="/api/project/task_dependency/update/"
                                     transport-update-data-type="json"
                                     transport-update-type="PUT"
                                     transport-create-url="/api/project/task_dependency/create/"
                                     transport-create-data-type="json"
                                     transport-create-type="POST"
                                     transport-destroy-url="/api/project/task_dependency/delete/"
                                     transport-destroy-data-type="json"
                                     transport-destroy-type="DELETE"
                                     :transport-parameter-map="dependencyParameterMap"
                                     schema-model-id="id"
                                     :schema-data="taskDependencyData"
                                     :schema-model-fields="dependencyfields">
    </gantt-dependency-data-source>

    <gantt ref="grantt"
                 data-source-ref="ganttdatasource1"
                 dependencies-data-source-ref="ganttdependencydatasource1"
                 :show-work-hours="false"
                 :show-work-days="false"
                 :snap="false"
                 :editable="true"
                 :editable-dependencyCreate="true"
                 :height="appBodyHeight"
           :resources="resources"
           :assignments="assignments">
      <gantt-view :type="'day'"></gantt-view>
      <gantt-view :type="'week'" :selected="true"></gantt-view>
      <gantt-view :type="'month'"></gantt-view>
      <gantt-column :field="'title'" :title="'标题'" :editable="true" :sortable="true"></gantt-column>
      <gantt-column :field="'resources'" :title="'Owner'" :editable="true" :sortable="true"></gantt-column>
      <gantt-column :field="'end'" :title="'截止日期'" :format="'{0:yyyy-MM-dd}'" :editable="false" :sortable="true"></gantt-column>

    </gantt>
  </div>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import { Gantt, GanttColumn, GanttView, GanttInstaller } from '@progress/kendo-gantt-vue-wrapper'
  import { DataSource,
    HierarchicalDataSource,
    GanttDataSource,
    GanttDependencyDataSource,
    PivotDataSource,
    SchedulerDataSource,
    TreeListDataSource,
    DataSourceInstaller } from '@progress/kendo-datasource-vue-wrapper'

  export default {
    name: 'projectTaskGannt',
    props: {
      projectID: {
        type: [Number,String],
        defalut: 0
      }
    },
    data () {
      return {
        resources: {
          field: "resources",
          dataColorField: "color",
          dataTextField: "name",
          dataSource: {
            transport: {
              read: {
                url: "/api/project/1/project_members",
                dataType: "json"
              }
            },
            schema: {
              model: {
                id: "id",
                fields: {
                  id: { from: "PMMember", type: "number" }
                }
              },
              data: function (resp) {
                return resp.result
              }
            }
          }
        },
        assignments: {
          dataTaskIdField: "TaskID",
          dataResourceIdField: "ResourceID",
          dataValueField: "Units",
          dataSource: {
            transport: {
              read: {
                url: "",
                dataType: "json",
                type: 'GET'
              },
              update: {
                url: "/api/project/task_owner/update/",
                dataType: "json",
                type: 'PUT'
              },
              destroy: {
                url: "/api/project/task_owner/delete/",
                dataType: "json",
                type: "DELETE"
              },
              create: {
                url: "/api/project/task_owner/create/",
                dataType: "json",
                type: "POST"
              },
              parameterMap: function(options, operation) {
                if (operation !== 'read') {
                  return { models: kendo.stringify(options.models || options) }
                }
              }
            },
            schema: {
              model: {
                id: "ID",
                fields: {
                  ID: { from: 'id', type: "number" },
                  ResourceID: { from: 'Owner', type: "number" },
                  Units: { from: 'Unit', type: "number" },
                  TaskID: { from: 'Task', type: "number" }
                }
              },
              data: function (resp) {
                let soucreData = resp.result.results
                if (!soucreData) {
                  soucreData = resp.result
                }
                return soucreData
              }
            },
//            filter: { field: 'ResourceID', operator: 'eq', value: '12' }
          }
        },
        fields: {
          id: { from: 'id', type: 'number' },
          orderId: { from: 'OrderID', type: 'number', validation: { required: true } },
          Status: { from: 'Status', type: 'number',defaultValue: 1, validation: { required: true } },
          parentId: { from: 'Parent', type: 'number', defaultValue: null, validation: { required: true } },
          start: { from: 'StartDate', type: 'date' },
          end: { from: 'DeadLine', type: 'date' },
          title: { from: 'Title', defaultValue: '', type: 'string' },
          percentComplete: { from: 'Progress', type: 'number' },
          summary: { from: 'HasChild', type: 'boolean', defaultValue: false },
          expanded: { from: 'Expandend', type: 'boolean', defaultValue: true }
        },
        dependencyfields: {
          id: { from: 'id', type: 'number' },
          predecessorId: { from: 'Predecessor', type: 'number' },
          successorId: { from: 'Successor', type: 'number' },
          type: { from: 'Type', type: 'number' }
        },
//        filter: { field: 'title', operator: 'contains', value: 'w' },
      }
    },
    computed: {
      ...mapGetters('task', ['taskChange','taskFilterStatus','taskFilterOwners','taskFilterKeyword','taskFilters']),
      ...mapGetters('projectglobal', ['projectVersion','rightSidePanelShow', 'taskViewMode']),
      ...mapGetters(['appBodyHeight','userInfo']),
      versionID: function () {
        return this.projectVersion
      },
      project: function () {
        let result = 0
        if( this.projectID )
        {
           result = this.projectID
        }
        return result
      },

      getTaskUrl: function () {
        return '/api/project/'+ this.project +'/version/0/project_tasks?page_size=10000'
      }

    },
    methods:
      {
        ...mapMutations('task', ['setTaskChange']),
        ...mapMutations('projectglobal', ['setViewDialogShow','setRightPanelShow']),

          taskResultData: function (resp) {
          let soucreData = resp.result.results
          if (!soucreData) {
            soucreData = resp.result
          }
          return soucreData
        },

        taskDependencyData: function (resp) {
          let soucreData = resp.result.results
          if (!soucreData) {
            soucreData = resp.result
          }
          return soucreData
        },

        onAddTask: function (e) {
//          this.setViewDialogShow(true)
//          e.preventDefault()
          console.log(e)
        },

        requestEnd: function (e) {
          console.log(e)
          if (e.action === 'add')
          {
            setTimeout(function () {
//              this.$refs.ganttdatasource1.kendoWidget().sync()
            })
//            this.getTasks(this.project,this.versionID)
//            this.$refs['grantt'].kendoWidget().dataSource.getByUid(e.items[0].uid).id=200
          }
        },

        onEditTask: function (e) {
          console.log(e)
        },

        onSelectTask: function (e) {

        },

        onTaskChange: function (e) {
        },

        parameterMap: function(options, operation) {
          let tempFormItem = options.models || options
          if (operation === 'read')
          {
            return {'ProjectID': this.project,'Version': this.versionID}
          }
          if (operation !== 'read') {
            tempFormItem.ProjectID = this.project
            tempFormItem.Version = this.versionID
            tempFormItem.WorkHours = 8
            tempFormItem.childTask= {}
            return {models: kendo.stringify(tempFormItem)}
          }
        },

        dependencyParameterMap: function (options, operation) {
          let tempFormItem = options.models || options
          if (operation === 'read')
          {
            return {'Version': this.versionID}
          }
          if (operation !== 'read') {
            return {models: kendo.stringify(tempFormItem)}
          }
        },

        loadAllTasks: function () {
          this.$axios.get(this.getTaskUrl).then(response => {
            console.log(response)
            return response.data.result.results
          }, response => {

          })
        }

      },
    created: function () {
      this.resources.dataSource.transport.read.url = '/api/project/' + this.project +'/project_members'
      this.assignments.dataSource.transport.read.url = '/api/project/task/task_owners?Version=' + this.versionID + '&page_size=10000'
    },
    mounted: function () {
    },
    watch: {
      versionID: function (value) {
        let parameters = {}
        parameters['Version'] = value
        this.$refs['grantt'].kendoWidget().dataSource.read()
      }
    },

    components: {
      Gantt,
      GanttView,
      GanttInstaller,
      Window,
      DataSource,
      HierarchicalDataSource,
      GanttDataSource,
      GanttDependencyDataSource,
      PivotDataSource,
      SchedulerDataSource,
      TreeListDataSource,
      GanttColumn
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .board-column-item {
    margin-bottom: 5px;
    margin-top: 5px;
    min-height: 74px;
    max-height: 200px;
    width: 280px;
  }

  .board-item-priority {
    width: 1px;
    display: inline-block;
    float: left;
    height:170px;
  }

  .board-item-body {
    width: 235px;
    display: inline-table;
    word-wrap: break-word;
    white-space: initial;
    padding: 10px;

  }

  .board-item-rightbar {
    display: inline-table;
  }

  .board-item-avatar {
    margin-right: 15px;
    margin-top: 10px;
  }

</style>
