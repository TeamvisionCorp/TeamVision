<template>
  <div>
    <button @click="newAction" id="22"
    ">+</button>
    <button @click="reduceAction" id="23">-</button>
    {{hello}}
  </div>
</template>

<script>
  import store from '../store/index.js'
  import { mapGetters, mapMutations, mapActions } from 'vuex'

  export default {
    name: 'HomeProjectWebpart',
    computed: {
      ...mapGetters(['mehuLabelID'])
    },
    methods: {
      ...mapMutations(['add', 'reduce']),
      ...mapActions(['addAction', 'reduceAction']),
      newAction: function (event) {

        var id = event.target.id
        console.log(window.innerHeight)
        this.add(1)
      }
    },
    data () {
      return {
        msg: 2
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  @import '../assets/teamcat/global/less/global';

</style>
