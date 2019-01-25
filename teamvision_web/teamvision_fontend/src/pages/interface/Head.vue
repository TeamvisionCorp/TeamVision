<template>
  <div class="app-body-head-default">
  <div class="app-body-header-bar-default">
          <div class="app-body-header-leftbar-default pull-left">
                  <ul class="app-body-head-menu">
                    <router-link to="/interface/mock" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
                      <a href="/interface/mock"><i class="fa fa-fw  fa-bus"></i>Mcok</a>
                    </router-link>
                    <router-link to="/interface/api" tag="li" active-class="app-body-head-menu-item-active" class="app-body-head-menu-item">
                      <a href="/interface/api"><i class="fa fa-fw  fa-bus"></i>API管理</a>
                    </router-link>
                   </ul>
          </div>
          <div class="app-body-header-rightbar-default pull-right">
            <!--<Avatar style="background-color: #32be77;margin-left:-100px;" icon="md-add" />-->
           </div>
  </div>
  </div>
</template>

<script>
  export default {
    name: 'EnvHead',
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
@import '../../components/layout/appBody';
@import '../../components/layout/appHead';
@import '../../assets/teamcat/global/less/global';

</style>
