
<template>
  <div>
    <Layout>
      <app-header></app-header>
      <app-body></app-body>
    </Layout>

  </div>
</template>

<script>
import AppHeader from './AppHead.vue'
import AppBody from './AppBody.vue'
export default{
  name: 'WebApp',
  components: {
    AppHeader,
    AppBody
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
</style>
