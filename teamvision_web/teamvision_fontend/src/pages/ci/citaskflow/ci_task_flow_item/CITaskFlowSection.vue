<template>
  <Card class="board-column" :dis-hover="true" :bordered="true" :shadow="false" >
    <slot name="column-header">
      <Card :bordered="false" :shadow="false" :dis-hover="true" class="board-column-title">{{ columnTitle }}</Card>
    </slot>
    <Scroll :on-reach-bottom="handleReachBottom"  :height="columnItemHeight">
      <draggable v-model="columnItems" :options="{group: group}" @end="onEnd">
        <transition-group class="dragable-area" :key="columnID" :id="columnID">
          <div v-for="element in columnItems" :key="element.id+''+element.UUID" :id="element.id">
            <slot :element="element">
            </slot>
          </div>
        </transition-group>

      </draggable>
    </Scroll>
  </Card>
</template>

<script>
  import draggable from 'vuedraggable'

  export default {
    name: 'FlowSection',
    props: {
      columnID: {
        type: Number,
        required: true
      },
      group: {
        type: String,
        required: true
      },
      itemList: {
        type: Array,
        required: true
      },
      columnTitle: {
        type: String,
        required: true
      }
    },
    data () {
      return {
        appBodyHeight: 863,
        columnItemHeight: 200,
        columnItems: this.itemList
      }
    },
    computed: {
//      columnItems: {
//        get: function (){
//          return this.itemList
//        },
//        set: function (value) {
//          this.itemList = value
//        }
//
//      }
    },
    components: {
      draggable
    },
    methods: {
      onEnd (event) {
        this.$emit('end', event)
        this.columnItemKey = new Date().getTime()
      },
      handleReachBottom () {
        this.$emit('reachBottom', this.columnID)
      }
    },
    watch: {
      itemList: function () {
        this.columnItems=this.itemList
      }
    },
    created: function () {
      this.columnItems=this.itemList

    },
    mounted: function () {
      this.columnItemHeight = document.getElementById('appBody').offsetHeight - 70
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .board-column{
    max-width:420px;
    width:23%;
    display: inline-table;
    background: #f5f7f9;
  }
  .board-column-title{
    background: #f5f7f9;
    margin-top:-15px;
    text-align: center;
  }
  .dragable-area{
    display: block;
    /*overflow-y: scroll;*/
    /*overflow-x: hidden;*/
    min-height:300px;
  }
</style>
