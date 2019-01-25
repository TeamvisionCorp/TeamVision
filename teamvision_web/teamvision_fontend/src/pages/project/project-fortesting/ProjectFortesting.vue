<template>
  <div>
    <board-column v-for="fortestinglist in fortestingForColumns" :key="fortestinglist.id" :columnID="fortestinglist.id" :group="fortestinglist.group"
                  v-bind:itemList.sync="fortestinglist.data" :columnTitle="fortestinglist.title+'-'+fortestinglist.count"
                  style="border:none" @end="onEnd" @reachBottom="onReachBottom">
      <template slot-scope="slotProps">
         <project-forteting-item :fortesting="slotProps.element" @view-fortesting="onViewFortesting"></project-forteting-item>
      </template>
    </board-column>
    <project-fortesting-create-dialog :fortestingID="fortestingItemID"></project-fortesting-create-dialog>
  </div>
</template>

<script>
  import draggable from 'vuedraggable'
  import { mapGetters, mapMutations, mapActions, mapState } from 'vuex'
  import BoardColumn from '../../../components/common/BoardColumn.vue'
  import ProjectFortestingCreateDialog from './ProjectFortestingCreateDialog.vue'
  import ProjectFortetingItem from './ProjectFortestingItem.vue'
  import { axiosSync } from './ProjectFortesting'

  export default {
    name: 'projectFortestingList',
    props: {
      projectID: {
        type: [Number,String],
        defalut: 0
      }
    },
    data () {
      return {
        columnItemHeight: 200,
        fortestingList: [],
        fortestingItemID: 0
      }
    },
    computed: {
      ...mapGetters('projectglobal', ['projectVersion','objectChange']),
      versionID: function () {
        return this.projectVersion
      },
      fortestingForColumns: function () {
        if (this.objectChange === true)
        {
          this.fortestingList = this.getColumnFortestings()
          this.setObjectChange(false)
        }
        return this.fortestingList
      },
      project: function () {
        let result = 0
        if( this.projectID )
        {
           result = this.projectID
          this.setProject(this.projectID)
        }
        return result
      }

    },
    methods:
      {
        ...mapMutations('projectglobal', ['setViewDialogShow', 'setObjectChange','setProject']),
        getColumnFortestings () {
          let result=[]
          let waitForFortestings = {id: 1, title: '待提测', group: 'ProjectFortesting', page: 1, count: 0, data: []}
          let commitedFortestings = {id: 2, title: '已提测', group: 'ProjectFortesting', page: 1, count: 0, data: []}
          let processFortestings = {id: 3, title: '测试中', group: 'ProjectFortesting', page: 1, count: 0, data: []}
          let finishedFortestings = {id: 4, title: '测试完成', group: 'ProjectFortesting', page: 1, count: 0, data: []}
          let releaseFortestings = {id: 5, title: '已上线', group: 'ProjectFortesting', page: 1, count: 0, data: []}
          result.push(waitForFortestings)
          result.push(commitedFortestings)
          result.push(processFortestings)
          result.push(finishedFortestings)
          result.push(releaseFortestings)
          for (let i = 0; i < result.length; i++)
          {
            let tempData = this.getFortestingList(this.project,this.versionID,result[i].id, result[i].page)
            tempData.then(function (value) {
              result[i].data = value.data.result.results
              result[i].count = value.data.result.count
            })
          }
          return result
        },
        onStart () {
          console.log('start')
        },
        onEnd (evt) {
          let toID = evt.to.getAttribute('id')
          let fromID = evt.from.getAttribute('id')
          let itemOldIndex = evt.oldIndex
          let itemNewIndex = evt.newIndex
          let itemID = evt.item.getAttribute('id')
          this.alterColumnData(fromID, toID, itemID, itemOldIndex, itemNewIndex)
          this.$axios.patch('/api/project/fortesting/'+itemID+'/update_status',{'Status': toID}).then(response => {
            if(response.data.result.Status)
            {
              this.$Message.success({
                content: response.data.result.message,
                duration: 10,
                closable: true
              })
            }

          }, response => {
            this.setObjectChange(true)
            this.$Message.error({
              content: response.data.result.message,
              duration: 10,
              closable: true
            })
          })

        },

        onRemove () {
          console.log('remove')
        },
        onMove () {
          console.log('move')
        },
        alterColumnData (fromID, toID, itemID, itemOldIndex, itemNewIndex) {
          let dragItem= null
          this.fortestingForColumns.forEach(function (fortestingList, index) {
             if(fortestingList.id === parseInt(fromID))
             {
               fortestingList.count=fortestingList.count-1
               for(let i=0; i<fortestingList.data.length; i++) {
                 if(fortestingList.data[i].id === parseInt(itemID))
                 {
                   dragItem=fortestingList.data[i]
                   fortestingList.data.splice(i, 1)
                   break
                 }
               }
             }
          })

          this.fortestingForColumns.forEach(function (fortestingList, index) {
            if(fortestingList.id === parseInt(toID))
            {
              fortestingList.count=fortestingList.count+1
              fortestingList.data.splice(itemNewIndex,0,dragItem)
            }
          })
        },
        onReachBottom (columnid) {
          for( let i=0; i < this.fortestingForColumns.length; i++ ) {
            if (this.fortestingForColumns[i].id === parseInt(columnid)) {
              let moreFortestings=[]
              let fortestings=this.fortestingForColumns
              this.fortestingForColumns[i].page=this.fortestingForColumns[i].page+1
              let tempData = this.getFortestingList(this.project,this.versionID,this.fortestingForColumns[i].id, this.fortestingForColumns[i].page)
              tempData.then(function (value) {

                moreFortestings=value.data.result.results
                fortestings[i].data.push(...moreFortestings)
              })
              break
            }
          }
        },
        getFortestingList  (projectID, versionID, status, page) {
          let url='/api/project/' + projectID + '/version/'+versionID+'/fortestings?Status=' + status + '&page=' + page
          let result = axiosSync(url,{},'get')
          return result
        },
        onFortestingItemClick (event) {
          this.setCreateDialogShow(true)
          let fortestingID = event.target.getAttribute('id')
          this.fortestingItemID = parseInt(fortestingID)
        },
        onViewFortesting (fortestingID)
        {
          this.setViewDialogShow(true)
          this.fortestingItemID = parseInt(fortestingID)
        }

      },
    created: function () {
      this.fortestingList = this.getColumnFortestings()
    },
    mounted: function () {
    },
    watch: {
      versionID: function (value) {
        this.fortestingList = this.getColumnFortestings()
      }

    },

    components: {
      draggable,
      BoardColumn,
      ProjectFortestingCreateDialog,
      ProjectFortetingItem
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
