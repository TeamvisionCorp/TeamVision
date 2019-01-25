<template>
  <Modal :value="responseCreateDialogShow" title="添加响应" :width="800" @on-cancel="cancel"
         :styles="{bottom:'20px',top: '50px'}">
    <div style="height:600px;overflow-y: scroll;overflow-x: hidden">
      <Form ref="responseCreate" :model="formItem" :label-width="80" :rules="ruleCustom">
        <FormItem label="响应描述" prop="Description">
          <Input v-model="formItem.Description" placeholder="响应描述"/>
        </FormItem>
        <FormItem label="响应值" prop="Response">
          <Input v-model="formItem.Response" type="textarea" :rows="12" placeholder="API返回值"/>
        </FormItem>
        <FormItem label="回调URL" prop="CallBackUrl">
          <Input v-model="formItem.CallBackUrl" type="textarea" :rows="6" placeholder="回调接口"/>
        </FormItem>
        <FormItem label="回调Method" prop="CallBackMethod">
          <Select v-model="formItem.CallBackMethod" :filterable="true" placeholder="回调请求方法">
            <Option v-for="method in httpMethodList " :key="method.id" :value="method.id">{{ method.label }}</Option>
          </Select>
        </FormItem>

        <!--<FormItem label="启用" prop="Enable">-->
        <!--<i-switch size="large" v-model="formItem.Enable">-->
        <!--<span slot="open">开启</span>-->
        <!--<span slot="close">关闭</span>-->
        <!--</i-switch>-->
        <!--</FormItem>-->

      </Form>
    </div>
    <div slot="footer">
      <Button v-if="isCreateResponse!==true" type="success" style="width: 80px; height:30px;" shape="circle"
              @click="addResponse('responseCreate')">保存
      </Button>
      <Button v-if="isCreateResponse" type="success" style="width: 80px; height:30px;" shape="circle"
              @click="addResponse('responseCreate')">添加
      </Button>
    </div>
  </Modal>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import { responseValidateRules } from './ResponseCreateDialog'
  import FormItem from '../../../../node_modules/iview/src/components/form/form-item.vue'
  import iSwitch from '../../../../node_modules/iview/src/components/switch/switch.vue'

  export default {
    name: 'responseCreateDialog',
    props: ['apiID', 'responseID'],
    data () {
      return {
        formItem: {
          ApiID: 0,
          Description: '',
          Response: '',
          CallBackUrl: '',
          CallBackMethod: 1,
          Enable: false
        },
        ruleCustom: {
          ...responseValidateRules
        },
        httpMethodList: [{
          id: 1,
          label: 'GET'
        },
          {
            id: 2,
            label: 'POST'
          },
          {
            id: 3,
            label: 'PUT'
          },
          {
            id: 4,
            label: 'PATCH'
          }, {
            id: 5,
            label: 'DELETE'
          }
        ],
      }

    },
    computed: {
      ...mapGetters('mockapi', ['responseCreateDialogShow','selectedApi']),

      isCreateResponse: function () {
        if (this.responseID === 0)
        {
          return true
        }
        else
        {
          return false
        }
      }
    },
    methods:
      {
        ...mapMutations('mockapi', ['setResponseCreateDialogShow', 'setResponseAdded']),

        addResponse (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {
              if (this.responseID ===0)
              {
                this.$axios.post('/api/interface/mock/responses', this.formItem).then(response => {
                  this.setResponseCreateDialogShow(false)
                  this.setResponseAdded(true)
                }, response => {
                  this.setResponseCreateDialogShow(false)
                  this.$Message.error({
                    content: '创建响应失败，请联系管理员或者重试',
                    duration: 10
                  })
                })
              }
              else
              {
                this.$axios.put('/api/interface/mock/response/'+this.responseID, this.formItem).then(response => {
                  this.setResponseCreateDialogShow(false)
                  this.setResponseAdded(true)
                }, response => {
                  this.setResponseCreateDialogShow(false)
                  this.$Message.error({
                    content: '保存响应失败，请联系管理员或者重试',
                    duration: 10
                  })
                })
              }
            }
          })
        },
        cancel () {
          this.setResponseCreateDialogShow(false)
        },

        loadResponse: function (responseID) {
          if (responseID+'' !== '0') {
            this.$axios.get('/api/interface/mock/response/' + responseID).then(response => {

              let resp = response.data.result
              this.formItem.ApiID = resp.ApiID
              this.formItem.Description = resp.Description
              this.formItem.Response = resp.Response
              this.formItem.CallBackUrl = resp.CallBackUrl
              this.formItem.CallBackMethod = resp.CallBackMethod
              this.formItem.Enable = resp.Enable
            }, response => {

            })
          } else {
            this.formItem.ApiID = this.apiID
            this.formItem.Description = ''
            this.formItem.Response = ''
            this.formItem.CallBackUrl = ''
            this.formItem.CallBackMethod = 1
            this.formItem.Enable = false
          }
        }

      },
    created () {
      this.formItem.ApiID = this.apiID
      this.loadResponse(this.responseID)
    },
    mounted () {

    },
    watch: {
      apiID: function () {
        this.formItem.ApiID = this.apiID
      },
      responseID: function () {
        this.loadResponse(this.responseID)
      }
    },
    components: {
      FormItem,
      iSwitch
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
