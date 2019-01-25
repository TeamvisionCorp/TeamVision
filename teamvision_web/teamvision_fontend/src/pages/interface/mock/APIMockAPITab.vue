<template>
  <div>
    <div style="height:25px;border-bottom: 1px solid honeydew">
        <span style="float: right;padding-right:10px;" class="cursor-hand">
          <Dropdown :transfer="true" style="border-radius: 0;" @on-click="onAddApiMenuClick">
          <Icon type="md-add-circle" :size="24" color="#32be77"/>
          <DropdownMenu slot="list">
            <DropdownItem name="api"><span style="font-size: 10px;">
              <Icon type="ios-paper"/> API</span></DropdownItem>
            <DropdownItem name="folder"><span style="font-size: 10px;">
              <Icon type="md-folder"/> 文件夹</span></DropdownItem>
          </DropdownMenu>
        </Dropdown>
        </span>
    </div>
    <div>
      <Tree :data="apiTreeData" style="text-align: left;" @on-select-change="onApiTreeNodeSelect"></Tree>
    </div>

    <Modal
      v-model="showApiAddDialog"
      :title="'添加' + formItem.titleLabel"
      @on-ok="apiAddOk"
      @on-cancel="apiAddCancel">
      <Form ref="apiCreateForm" :label-width="80" :model="formItem">
        <FormItem label="名称" prop="ApiTitle">
          <Input v-model="formItem.ApiTitle" placeholder="API名称"/>
        </FormItem>
        <FormItem v-if="formItem.ApiType===1" label="API路径" prop="ApiPath">
          <Input v-model="formItem.ApiPath" placeholder="API路径" />
        </FormItem>
        <FormItem v-if="formItem.ApiType===1" label="HTTPMethod" prop="HttpMethod">
          <Select v-model="formItem.CallBackMethod" :filterable="true" placeholder="回调请求方法">
          <Option v-for="method in httpMethodList " :key="method.id" :value="method.id">{{ method.label }}</Option>
          </Select>
        </FormItem>
        <!--<FormItem v-if="formItem.ApiType===1" label="Handler" prop="MockHandler">-->
          <!--<Select v-model="formItem.CallBackMethod" :filterable="true" placeholder="回调请求方法">-->
          <!--<Option v-for="method in httpMethodList " :key="method.id" :value="method.id">{{ method.label }}</Option>-->
            <!--</Select>-->
        <!--</FormItem>-->
        <FormItem v-if="formItem.ApiType===1" label="描述" prop="Description">
          <Input v-model="formItem.Description" type="textarea" placeholder="API描述" />
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
  import store from '../../../store/index.js'
  import { mapGetters, mapMutations } from 'vuex'

  export default {
    name: 'mockAPIManagement',
    data () {
      return {
        selectNode: [],
        showApiAddDialog: false,
        apiTreeRoot: null,
        formItem: {
          ApiTitle: '',
          ApiPath: '',
          ApiType: 1,
          HttpMethod: 1,
          MockHandler: 1,
          Description: '',
          Enable: 1
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
        ],
        apiCreateRule: {
          ApiTitle: [
            {type: 'string', message: '名称不能超过50个字符！', required: true, min: 1, max: 50, trigger: 'blur'}
          ],
          ApiPath: [
            {type: 'string', message: '路径不能超过1000个字符！', required: true, min: 1, max: 1000, trigger: 'blur'}
          ]
        },
        apiTree: [
          {
            title: '全部接口',
            expand: true,
            render: (h, {root, node, data}) => {
              this.apiTreeRoot = root
              return h('span', {
                style: {
                  display: 'inline-block',
                  width: '100%'
                }
              }, [
                h('span', [
                  h('Icon', {
                    props: {
                      type: 'ios-folder-outline'
                    },
                    style: {
                      marginRight: '8px',
                      fontSize: '18px'
                    }
                  }),
                  h('span', data.title)
                ]),
              ])
            },
            children: []
          }
        ]
      }
    },

    computed: {

      isShowAPIAddDialog: function () {
        return this.showApiAddDialog
      },

      apiTreeData: function () {
        return this.apiTree
      }
    },

    methods: {
      ...mapMutations('mockapi', ['setSelectedApi']),
      append (data, apiData) {
        const children = data.children || []
        let tempNode = {
          id: apiData.id,
          type: apiData.ApiType,
          title: apiData.ApiTitle,
          expand: true
        }
        children.push(tempNode)
        this.$set(data, 'children', children)
      },

      remove (root, node, data) {
        const parentKey = root.find(el => el === node).parent
        const parent = root.find(el => el.nodeKey === parentKey).node
        const index = parent.children.indexOf(data)
        parent.children.splice(index, 1)
      },

      onAddApiMenuClick: function (name) {
        if (name === 'api') {
          this.formItem.titleLabel = 'API'
          this.formItem.ApiType = 1
        }
        if (name === 'folder') {
          this.formItem.titleLabel = '文件夹'
          this.formItem.ApiType = 2
        }
        if (this.selectNode.length > 0) {
          if (this.selectNode[0].type + '' === '2') {
            this.showApiAddDialog = true
          }
          else {
            this.$Message.error({
              content: '不能为API接口添加子项目！',
              duration: 10
            })
          }
        }
        else {
          this.showApiAddDialog = true
        }
//        else
//        {
//          this.$Message.error({
//            content: '请先选择一个文件夹！',
//            duration: 10
//          })
//        }
      },

      onApiTreeNodeSelect: function (datas) {
        this.selectNode = datas
        this.setSelectedApi(datas[0].id)
      },

      newApi: function () {
        this.$axios.post('/api/interface/mock/apis', this.formItem).then(response => {
          console.log(this.selectNode.length)
          if (this.selectNode.length > 0) {
            this.append(this.selectNode[0], response.data.result)
          }
          else {
            this.append(this.apiTreeData[0], response.data.result)
          }
        }, response => {
        })
      },

      loadApiTree: function () {
        this.$axios.get('/api/interface/mock/api_tree?Parent=0').then(response => {
          this.apiTree[0].children = response.data.result
        }, response => {
        })
      },

      apiAddOk: function () {
        this.$refs['apiCreateForm'].validate((valid) => {
          if (valid) {
            if (this.selectNode.length > 0) {
              this.formItem['Parent'] = this.selectNode[0].id
              this.newApi()
            }
            else {
              this.formItem['Parent'] = 0
              this.newApi()
            }
            this.showApiAddDialog = false
          }
        })
      },

      apiAddCancel: function () {
        this.showApiAddDialog = false
      }
    },
    created: function () {
      this.loadApiTree()
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
