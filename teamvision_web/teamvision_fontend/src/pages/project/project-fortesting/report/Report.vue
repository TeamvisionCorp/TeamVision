<template>
  <div :style="'overflow:scroll;height:'+reportContainerHeight+'px'">
   <bvt-report v-if="reportName ==='bvt'" :projectID="projectID" :fortestingID="fortestingID"></bvt-report>
    <progress-report v-if="reportName ==='progress'" :projectID="projectID" :fortestingID="fortestingID"></progress-report>
    <testing-complete v-if="reportName ==='testcomplete'" :projectID="projectID" :fortestingID="fortestingID"></testing-complete>
  </div>
</template>

<script>
  import ICol from '../../../../../node_modules/iview/src/components/grid/col.vue'
  import { VueEditor } from 'vue2-editor'
  import store from '../../../../store/index.js'
  import { mapGetters, mapMutations } from 'vuex'
  import BvtReport from './BVT.vue'
  import ProgressReport from './Progress.vue'
  import TestingComplete from './TestingComplete.vue'

  export default {
    name: 'FortestingBVTReport',
    props: ['projectID', 'fortestingID', 'reportName'],
    data () {
      return {
        single: false,
        TestingAdvice: '',
        value: '',
        editorToolBar: [
          ['bold', 'italic', 'underline'],
          [{'list': 'ordered'}, {'list': 'bullet'}], [{'color': []}, {'background': []}],
        ],
        cityList: [
          {
            value: 'New York',
            label: 'New York'
          },
          {
            value: 'London',
            label: 'London'
          },
          {
            value: 'Sydney',
            label: 'Sydney'
          },
          {
            value: 'Ottawa',
            label: 'Ottawa'
          },
          {
            value: 'Paris',
            label: 'Paris'
          },
          {
            value: 'Canberra',
            label: 'Canberra'
          }
        ],
        model11: '',
        model12: []
      }
    },
    computed: {
      ...mapGetters(['appBodyHeight']),
      reportContainerHeight: function () {
        return this.appBodyHeight - 33
      }
    },
    components: {VueEditor, ICol, TestingComplete, ProgressReport, BvtReport}
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  table, th, td {
    border: 1px solid lightgray;
    padding: 2px;
    padding-left: 5px;
    padding-right: 5px;
  }
</style>
