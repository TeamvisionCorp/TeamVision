<template>
  <div class="app-body-head-default">
      <component :is="headComponents[menuLabelID]"></component>
  </div>
</template>

<script>
  import MyHead from '../../pages/home/Head.vue'
  import EnvHead from '../../pages/interface/Head.vue'

  export default {
    name: 'BodyHead',
    data() {
      return {
        headComponents: {1: 'MyHead',5:'EnvHead'}
      }
    },
    computed: {
    },
    components: {
      MyHead,
      EnvHead
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  @import '../../assets/teamcat/global/less/global';
</style>
