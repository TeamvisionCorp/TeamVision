<template>
  <div style="padding-left: 5px;padding-right:5px;margin-top: -10px">
    <Split v-model="splitH" :min="0.1" :max="0.3" :style="'height:'+envContainerHeight+'px;'">
      <div slot="left">
        <Tabs>
          <TabPane label="API 接口" icon="md-aperture" style="margin-top: -10px;">
            <mock-a-p-i-management></mock-a-p-i-management>
          </TabPane>
          <!--<TabPane label="NewTree" icon="md-aperture" style="margin-top: -10px;">-->
            <!--<api-admin-tree  @onAddApi="onSelected"></api-admin-tree>-->
          <!--</TabPane>-->
        </Tabs>
      </div>
      <div slot="right" class="demo-split-pane" style="padding:20px">
        <div v-if="currentApiType === 1">
          <Split v-model="splitV" :min="0.05" :max="0.5" :style="'height:'+envContainerHeight+'px;'" mode="vertical">
            <env-mock-a-p-i-detail slot="top" :apiID="selectedApi"></env-mock-a-p-i-detail>
            <Divider style="margin: 12px 0px"></Divider>
            <env-mock-response slot="bottom" :apiID="selectedApi" :height="respContainerHeight"></env-mock-response>
          </Split>
        </div>
        <!--<div>-->
          <!--<span><Alert show-icon  type="error" style="text-align: left" closable>点击左侧边栏选择API</Alert></span>-->
        <!--</div>-->
      </div>
    </Split>
  </div>
</template>

<script>
  import store from '../../../store/index.js'
  import { mapGetters, mapMutations, mapActions } from 'vuex'
  import mockAPIManagement from './APIMockAPITab.vue'
  import envMockAPIDetail from './APIMockAPIDetail.vue'
  import envMockResponse from './APIMockResponse.vue'
  import ApiAdminTree from '../api-admin/ApiAdminTree.vue'

  export default {
    name: 'EnvMockWebpart',
    data () {
      return {
        splitH: 0.18,
        splitV: 0.4,
        currentApiType: 0
      }
    },
    computed: {
      ...mapGetters(['appBodyHeight']),
      ...mapGetters('mockapi', ['selectedApi']),
      envContainerHeight: function () {
        return this.appBodyHeight-15
      },
      respContainerHeight: function () {
        return this.envContainerHeight-this.envContainerHeight*this.splitV
      }
    },
    methods: {
      ...mapMutations('mockapi',['setResponseCreateDialogShow']),

      loadCurrentApi: function () {
        this.$axios.get('/api/interface/mock/api/'+this.selectedApi).then(response => {
          this.currentApiType = response.data.result.ApiType
        }, response => {

        })
      },

      onSelected: function (id) {
        console.log('parent')
        console.log(id)
      }

    },
    watch: {
      selectedApi: function () {
         this.loadCurrentApi()
      }
    },
    components: {
      mockAPIManagement,
      envMockAPIDetail,
      envMockResponse,
      ApiAdminTree
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
