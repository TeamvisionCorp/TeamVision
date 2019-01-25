<template>
  <div :style="'height:'+historyContainerHeight+'px'+'; overflow-y:scroll;padding-left:10px;padding-right:10px;'">
    <flow-history-item :flowID="flowID"></flow-history-item>
  </div>
</template>

<script>
  import store from '../../../../store/index.js'
  import { mapGetters, mapMutations} from 'vuex'
  import flowHistoryItem from './CITaskFlowHistoryItem.vue'
  export default {
    name: 'flowHistory',
    props: ['flowID'],
    data () {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    },
    computed: {
    ...mapGetters(['appBodyHeight']),
    historyContainerHeight: function () {
        return  this.appBodyHeight-33
      },
    },
    components: {
      flowHistoryItem
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
