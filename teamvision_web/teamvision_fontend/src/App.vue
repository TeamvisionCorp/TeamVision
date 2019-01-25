<template>
  <div id="app">
    <web-app/>
  </div>
</template>

<script>
  import WebApp from './components/layout/WebApp.vue'

  export default {
    components: {
      WebApp
    }
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>
