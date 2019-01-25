<template>
  <div>
    <gantt-data-source ref="ganttdatasource1"
                           :transport-read-url="'/api/project/'+ project +'/version/' + versionID + '/project_tasks?page_size=10000'"
                           transport-read-data-type="json"
                           :transport-update-url="serviceRoot + '/GanttTasks/update'"
                           transport-update-data-type="jsonp"
                           :transport-create-url="serviceRoot + '/GanttTasks/create'"
                           transport-create-data-type="jsonp"
                           :transport-destroy-url="serviceRoot + '/GanttTasks/destroy'"
                           transport-destroy-data-type="jsonp"
                           :transport-parameter-map="parameterMap"
                           schema-model-id="id"
                           :schema-model-fields="fields"
                           :resources="resources"
                           @change="onTaskChange"
                           :schema-data="testdata"
                           :assignments="assignments">
    </gantt-data-source>

    <gantt-dependency-data-source ref="ganttdependencydatasource1"
                                     :transport-read-url="serviceRoot + '/GanttDependencies'"
                                     transport-read-data-type="jsonp"
                                     :transport-update-url="serviceRoot + '/GanttDependencies/update'"
                                     transport-update-data-type="jsonp"
                                     :transport-create-url="serviceRoot + '/GanttDependencies/create'"
                                     transport-create-data-type="jsonp"
                                     :transport-destroy-url="serviceRoot + '/GanttDependencies/destroy'"
                                     transport-destroy-data-type="jsonp"
                                     :transport-parameter-map="parameterMap"
                                     schema-model-id="id"
                                     :schema-model-fields="dependencyfields">
    </gantt-dependency-data-source>

    <gantt id="gantt"
                 data-source-ref="ganttdatasource1"
                 dependencies-data-source-ref="ganttdependencydatasource1"
                 :show-work-hours="false"
                 :show-work-days="false"
                 :snap="false"
                 :editable="false"
                 :height="appBodyHeight"
                 :resources="resources"
                 @add="onAddTask"
                 @edit="onEditTask"
                 @change="onSelectTask"
                 :assignments="assignments">
      <gantt-view :type="'day'"></gantt-view>
      <gantt-view :type="'week'" :selected="true"></gantt-view>
      <gantt-view :type="'month'"></gantt-view>
      <gantt-column :field="'title'" :title="'标题'" :editable="true" :sortable="true"></gantt-column>
      <!--<gantt-column :field="'resources'" :title="'Owner'" :editable="true" :sortable="true"></gantt-column>-->
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
        columnItemHeight: 200,
        taskItemID: 0,
        serviceRoot: 'https://demos.telerik.com/kendo-ui/service',
        resources: {
          field: "resources",
          dataColorField: "Color",
          dataTextField: "Name",
          dataSource: {
            transport: {
              read: {
                url: "https://demos.telerik.com/kendo-ui/service/GanttResources",
                dataType: "jsonp"
              }
            },
            schema: {
              model: {
                id: "id",
                fields: {
                  id: { from: "ID", type: "number" }
                }
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
                url: "https://demos.telerik.com/kendo-ui/service/GanttResourceAssignments",
                dataType: "jsonp"
              },
              update: {
                url: "https://demos.telerik.com/kendo-ui/service/GanttResourceAssignments/Update",
                dataType: "jsonp"
              },
              destroy: {
                url: "https://demos.telerik.com/kendo-ui/service/GanttResourceAssignments/Destroy",
                dataType: "jsonp"
              },
              create: {
                url: "https://demos.telerik.com/kendo-ui/service/GanttResourceAssignments/Create",
                dataType: "jsonp"
              },
              parameterMap: function(options, operation) {
                if (operation !== "read") {
                  return { models: kendo.stringify(options.models || [options]) };
                }
              }
            },
            schema: {
              model: {
                id: "ID",
                fields: {
                  ID: { type: "number" },
                  ResourceID: { type: "number" },
                  Units: { type: "number" },
                  TaskID: { type: "number" }
                }
              }
            },
//            filter: { field: 'ResourceID', operator: 'eq', value: '12' }
          }
        },
        fields: {
          id: { from: 'ID', type: 'number' },
          orderId: { from: 'Creator', type: 'number', validation: { required: true } },
          parentId: { from: 'Parent', type: 'number', defaultValue: null, validation: { required: true } },
          start: { from: 'StartDateFormat', type: 'date' },
          end: { from: 'DeadLine', type: 'date' },
          title: { from: 'Title', defaultValue: '', type: 'string' },
          percentComplete: { from: 'Progress', type: 'number' },
          summary: { from: 'Tags', type: 'boolean',defaultValue: false },
          expanded: { from: 'Expanded', type: 'boolean', defaultValue: true }
        },
        dependencyfields: {
          id: { from: 'ID', type: 'number' },
          predecessorId: { from: 'PredecessorID', type: 'number' },
          successorId: { from: 'SuccessorID', type: 'number' },
          type: { from: 'Type', type: 'number' }
        },
        filter: { field: 'title', operator: 'contains', value: 'w' }
      }
    },
    computed: {
      ...mapGetters('task', ['taskChange','taskFilterStatus','taskFilterOwners','taskFilterKeyword','taskFilters']),
      ...mapGetters('projectglobal', ['projectVersion','rightSidePanelShow', 'taskViewMode']),
      ...mapGetters(['appBodyHeight']),
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
      }

    },
    methods:
      {
        ...mapMutations('task', ['setTaskChange']),
        ...mapMutations('projectglobal', ['setViewDialogShow','setRightPanelShow']),

        onDataBinding: function (ev) {
          console.log('Gantt is about to be bound!')
        },
        onDataBound: function (ev) {
          console.log('Gantt is now bound!')
        },

        testdata: function (resp) {
          console.log(resp)
          return resp.result.results
        },

        onAddTask: function (e) {
//          this.setViewDialogShow(true)
//          e.preventDefault()
          console.log(e)
        },

        onEditTask: function (e) {
          console.log(e)
        },

        onSelectTask: function (e) {

        },

        onTaskChange: function (e) {
          console.log(e)
          e.preventDefault()
        },

        parameterMap: function(options, operation) {
          if (operation !== 'read') {
            return {models: kendo.stringify(options.models || [options])}
          }
        }

      },
    created: function () {
    },
    mounted: function () {
    },
    watch: {
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
