<template>
  <Card dis-hover :bordered="false">
    <p slot="title" style="text-align: left">API信息</p>
    <Form ref="apiCreateForm" :label-width="80" :model="formItem">
      <FormItem label="API名称" prop="APITitle" style="text-align: left;width:500px;">
        <label-editor-input @updateValue="updateApiTitle" placeHolder="API名称长度不能超过50个字符！"
                            :displayText="formItem.ApiTitle"></label-editor-input>
      </FormItem>
      <Row>
        <Col span="12">
        <FormItem label="API路径" prop="APIPath" style="max-width: 500px; margin-right: 20px; text-align: left">
          <label-editor-input @updateValue="updateApiPath" placeHolder="API路径不能为空！"
                              :displayText="formItem.ApiPath"></label-editor-input>
        </FormItem>
        </Col>
        <Col span="12">
        <FormItem label="HTTPMethod" prop="HttpMethod" style="max-width: 300px;margin-right: 20px; text-align: left">
          <label-editor-select @updateValue="updateHttpMethod" :displayText="formItem.HttpMethod" :value="formItem.HttpMethod"
                               :optionList="httpMethodList"></label-editor-select>
        </FormItem>
        </Col>
      </Row>
      <FormItem label="Handler" prop="MockHandler" style="max-width: 500px; text-align: left">
        <label-editor-select @updateValue="updateHandler" displayText="DefaultHandler" :value="formItem.MockHandler"
                             :optionList="handlerList"></label-editor-select>
      </FormItem>
      <FormItem label="描述" prop="Description" style="text-align: left;">
        <label-editor-text-area @updateValue="updateDesc" placeHolder="添加点描述信息吧！"
                                :displayText="formItem.Description"></label-editor-text-area>
      </FormItem>
    </Form>
  </Card>
</template>

<script>
  import store from '../../../store/index.js'
  import { mapGetters, mapMutations, mapActions } from 'vuex'
  import labelEditorInput from '../../../components/common/LabelEditor-Input.vue'
  import labelEditorSelect from '../../../components/common/LabelEditor-Select.vue'
  import labelEditorTextArea from '../../../components/common/LabelEditor-TextArea.vue'

  export default {
    name: 'envMockAPIDetail',
    props: ['apiID'],
    data () {
      return {
        formItem: {
          ApiTitle: '',
          ApiPath: '',
          HttpMethod: 'GET',
          MockHandler: 1,
          Description: ''
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
        handlerList: [{
          id: 1,
          label: 'DefaultHandler'
        }
        ]
      }
    },
    computed: {
      selectApi: function () {
        return this.apiID
      }
    },
    methods: {
      updateApiTitle: function (newValue) {
        this.formItem.ApiTitle = newValue
        this.updateApi(this.selectApi,'ApiTitle',newValue)
      },
      updateApiPath: function (newValue) {
        this.formItem.ApiPath = newValue
        this.updateApi(this.selectApi,'ApiPath',newValue)
      },
      updateHttpMethod: function (newValue) {
//        this.formItem.HttpMethod = newValue
        this.updateApi(this.selectApi,'HttpMethod',newValue)
      },
      updateHandler: function (newValue) {
//        this.formItem.MockHandler = newValue
        this.updateApi(this.selectApi,'MockHandler',newValue)
      },
      updateDesc: function (newValue) {
        this.formItem.Description = newValue
        this.updateApi(this.selectApi,'Description',newValue)
      },

      loadApiInfo: function (id) {
        this.$axios.get('/api/interface/mock/api/' + id).then(response => {
          let api = response.data.result
          this.formItem.ApiTitle = api.ApiTitle
          this.formItem.ApiPath = api.ApiPath
          this.formItem.HttpMethod = api.http_method_name
          this.formItem.Description = api.Description
        }, response => {
        })
      },

      updateApi: function (id, field, value) {
        let parameter={}
        parameter[field] = value
        this.$axios.patch('/api/interface/mock/api/' + id, parameter).then(response => {
          console.log(response)
        }, response => {
        })
      }

    },
    created: function () {
      this.loadApiInfo(this.apiID)
    },
    components: {
      labelEditorInput,
      labelEditorSelect,
      labelEditorTextArea
    },
    watch: {
      apiID: function () {
        this.loadApiInfo(this.apiID)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>

