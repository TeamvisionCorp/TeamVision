<template>
  <Card dis-hover :bordered="false">
    <p slot="title" style="text-align: left;height:24px;padding-bottom:5px;padding-right:50px;">
      <span>响应值</span>
      <span style="padding-left:10px;" class="cursor-hand" @click="onAddResponseClick">
                    <Icon type="md-add-circle" color="#32be77" :size="24"/>
                   </span>
    </p>
    <div :style="'height:'+responseContainerHeight+'px; overflow-y:scroll'">
      <span v-if="responseList.length ===0">还没有添加响应值，请添加</span>
      <Row v-if="item.Enable" style="text-align: left; border-bottom: 1px solid #f5f7f9;height:40px;padding-top:10px;"
           :id="item.id" :key="item.id" v-for="item in responseList">
        <Col :span="12" style="padding-left:20px;font-size: 12px;">
        {{ item.Description }}</Col>
        <Col :span="6" offset="6">
        <i-switch size="large" v-model="item.Enable" :id="item.id" style="margin-right: 20px;"
                  @on-change="onResponseEnable">
          <span slot="open">开启</span>
          <span slot="close">关闭</span>
        </i-switch>
        <ButtonGroup shape="circle" size="small">
          <Button icon="ios-create" @click="onEditResponse(item.id)"></Button>
          <Button icon="ios-trash" @click="onDeleteResponse(item.id)"></Button>
        </ButtonGroup>
        </Col>
      </Row>
      <Row v-if="item.Enable!==true"
           style="text-align: left; border-bottom: 1px solid #f5f7f9;height:40px;padding-top:10px;" :key="item.id"
           v-for="item in responseList">
        <Col :span="12" style="padding-left:20px;font-size: 12px;">
        {{ item.Description }}</Col>
        <Col :span="6" offset="6">
        <i-switch :id="item.id" size="large" v-model="item.Enable" style="margin-right: 20px;"
                  @on-change="onResponseEnable">
          <span slot="open">开启</span>
          <span slot="close">关闭</span>
        </i-switch>
        <ButtonGroup shape="circle" size="small">
          <Button icon="ios-create" @click="onEditResponse(item.id)"></Button>
          <Button icon="ios-trash" @click="onDeleteResponse(item.id)"></Button>
        </ButtonGroup>
        </Col>
      </Row>
    </div>
    <response-create-dialog :apiID="selectApiID" :responseID="currentResponseID"></response-create-dialog>
  </Card>
</template>

<script>
  import store from '../../../store/index.js'
  import { mapGetters, mapMutations, mapActions } from 'vuex'
  import responseCreateDialog from './ResponseCreateDialog.vue'
  import iSwitch from '../../../../node_modules/iview/src/components/switch/switch.vue'

  export default {
    name: 'envMockResponse',
    props: ['apiID', 'height'],
    data () {
      return {
        data1: true,
        responses: [],
        selectApiID: 0,
        currentResponseID: 0
      }
    },

    computed: {
      ...mapGetters('mockapi', ['responseAdded']),
      ...mapGetters(['appBodyHeight']),
      responseContainerHeight: function () {
        return this.height - 81 - 16
      },
      responseList: function () {
        if (this.responseAdded) {
          this.loadResponse(this.appID)
          this.setResponseAdded(false)
        }
        return this.responses
      }
    },

    methods: {
      ...mapMutations('mockapi', ['setResponseCreateDialogShow', 'setResponseAdded']),

      onAddResponseClick: function () {
        this.setResponseCreateDialogShow(true)
        this.currentResponseID = 0
      },

      onResponseEnable: function (value) {
        let responseID = event.target.id
        if (value) {
          for (let i = 0; i < this.responseList.length; i++) {
            if (this.responseList[i].Enable  && this.responseList[i].id!=responseID) {
              this.responseList[i].Enable = false
              this.$axios.patch('/api/interface/mock/response/' + this.responseList[i].id, {Enable: false}).then(response => {
              }, response => {
              })
            }
          }
          this.$axios.patch('/api/interface/mock/response/' + responseID, {Enable: value}).then(response => {
          }, response => {
          })
        }
      },

      onDeleteResponse: function (responseID) {
        this.$Modal.confirm({
          title: '删除确认',
          content: '请确认要删除响应值吗？',
          onOk: () => {
            this.$axios.delete('/api/interface/mock/response/' + responseID).then(response => {
               this.loadResponse()
            }, response => {
            })
          },
          onCancel: () => {
          }
        });
      },

      onEditResponse: function (responseID) {
        this.currentResponseID = responseID
        this.setResponseCreateDialogShow(true)

      },
      loadResponse: function (apiID) {
        this.$axios.get('/api/interface/mock/responses?ApiID=' + this.apiID).then(response => {
          this.responses = response.data.result
        }, response => {

        })
      }

    },
    created: function () {
      this.selectApiID = this.apiID
      this.loadResponse(this.ApiID)
    },
    watch: {
      apiID: function () {
        this.selectApiID = this.apiID
        this.loadResponse(this.apiID)
      }
    },
    components: {
      responseCreateDialog,
      iSwitch
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
