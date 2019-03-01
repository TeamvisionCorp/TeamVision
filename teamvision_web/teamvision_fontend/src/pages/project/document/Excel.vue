<template>
  <div id="vueapp" class="vue-app">
    <spreadsheet ref="spreadsheet" :columns="50" :rows="500"   :toolbar-home="toolbar" :sheetsbar="true"  @changeFormat="onChange" @change="onChange">
      <spreadsheet-sheet :name="'Products'" :sheets-rows-cells-enable="false"
                               :data-source="datasource"
                               :rows="rows"
                               :columns="columns">
      </spreadsheet-sheet>
    </spreadsheet>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapActions, mapState } from 'vuex'
import { Spreadsheet,
  SpreadsheetSheet,
  SpreadsheetInstaller } from '@progress/kendo-spreadsheet-vue-wrapper'

export default {
    name: 'projectTaskList',

    data () {
      return {
        rows: [],
        columns: [],
        datasource: {
          transport: {
            read: function (options) {
//              $.ajax({
//                url: "https://demos.telerik.com/kendo-ui/service/Products/",
//                dataType: "jsonp",
//                success: function (result) {
//                  options.success(result);
//                },
//                error: function (result) {
//                  options.error(result);
//                }
//              });
            },
            submit: function (options) {
              console.log(options)
//              $.ajax({
//                url: "https://demos.telerik.com/kendo-ui/service/Products/Submit",
//                data: { models: kendo.stringify(e.data) },
//                contentType: "application/json",
//                dataType: "jsonp",
//                success: function (result) {
//                  e.success(result.Updated, "update");
//                  e.success(result.Created, "create");
//                  e.success(result.Destroyed, "destroy");
//                },
//                error: function (xhr, httpStatusMessage, customErrorMessage) {
//                  alert(xhr.responseText)
//                }
//              });
            }
          },
//          batch: true,
//          schema: {
//            model: {
//              id: "ProductID",
//              fields: {
//                ProductID: { type: "number" },
//                ProductName: { type: "string" },
//                UnitPrice: { type: "number" },
//                Discontinued: { type: "boolean" },
//                UnitsInStock: { type: "number" }
//              }
//            }
//          }
        }
      }
    },
    computed: {
      ...mapGetters('task', ['projectVersion','taskChange']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight
      },
      toolbar: function () {
        return [
            {
            type: "button",
            text: "保存",
            showText: "both",
            icon: "k-icon k-i-save",
            click: () => {
              console.log(this.$refs['spreadsheet'].kendoWidget().toJSON())
            }
            },
          'open',
          'exportAs',
          ['cut', 'copy', 'paste'],
          ['bold', 'italic', 'underline'],
          'backgroundColor', 'textColor',
          'borders',
          'fontSize', 'fontFamily',
          'alignment',
          'textWrap',
          ['formatDecreaseDecimal', 'formatIncreaseDecimal'],
          'format',
          'merge',
          'freeze',
          'filter'
        ]
      },

      rowCounts: function () {
        return this.rows.length+1
      }
    },
    methods:
      {
        ...mapMutations(['setAppHeadShow', 'setAppBodyTop', 'setAppBodyHeight']),
        ...mapMutations('task', ['setViewDialogShow', 'setTaskChange']),
        onChange: function (e) {
          let sheet = this.$refs['spreadsheet'].kendoWidget().toJSON()
          console.log(kendo.stringify(sheet))
        }

      },
    created: function () {
      this.setAppHeadShow(false)
      this.setAppBodyTop(0)
      let windowHeight=window.innerHeight
      this.setAppBodyHeight(windowHeight)
    },
    mounted: function () {
      let spreadsheet = this.$refs.spreadsheet.kendoWidget()
      let windowHeight=window.innerHeight
      spreadsheet.element.css('height', windowHeight+'px')
      spreadsheet.element.css('width', '100%')
      spreadsheet.element.css('padding-left', '2px')
      spreadsheet.resize()
      let dataSource = {activeSheet:'Products',sheets:[{name:'Products',rows:[{index:0,height:35,cells:[{value:'sfd',background:'#ea157a',fontSize:26,'index':0},{'value':'fsda','background':'#ea157a','fontSize':26,'index':1},{'value':'fsda','background':'#ea157a','fontSize':26,'index':2},{'value':'fsda','background':'#ea157a','fontSize':26,'index':3},{'value':'fsda','background':'#ea157a','fontSize':26,'index':4},{'value':'fdsa','background':'#ea157a','fontSize':26,'index':5}]},{'index':3,'cells':[{'value':'fsdfds','index':6}]},{'index':15,'cells':[{'background':'#ea157a','index':6}]}],'columns':[],'selection':'G4:G4','activeCell':'G4:G4','frozenRows':0,'frozenColumns':0,'showGridLines':true,'mergedCells':[],'hyperlinks':[],'defaultCellStyle':{'fontFamily':'Arial','fontSize':'12'}}],'names':[],'columnWidth':64,'rowHeight':20}
      spreadsheet.fromJSON(dataSource)
      console.log(spreadsheet)
    },
    watch: {

    },

    components: {
      Spreadsheet,
      SpreadsheetSheet,
      SpreadsheetInstaller
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style src="../../../../node_modules/handsontable-pro/dist/handsontable.full.css"></style>
<style  lang="less">
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
  #hot-preview {
    width: 100%;
    height: 100%;
    overflow: scroll;
    padding-left:10px;
    padding-right:10px;
  }

  button{
    margin: 20px 20px;
  }
  .handsontable .currentRow {
    background-color: #E7E8EF;
  }

  .handsontable .currentCol {
    background-color: #F9F9FB;
  }
  #test-hot {
    width: 800px;
    height: 800px;
    overflow: scroll;
  }
</style>
