<template>
  <Modal :value="projectCreateDialogShow" title="添加新项目" :width="600" @on-ok="addProject" @on-cancel="cancel"   :styles="{bottom:'20px',top: '50px'}">
    <div :style="'height:' + containerHeight + 'px;overflow-y: scroll;overflow-x: hidden'">
      <Form  ref="projectCreate" :model="formItem" :label-width="80" :rules="ruleCustom">
        <FormItem label="项目名称" prop="PBTitle">
          <Input v-model="formItem.PBTitle" placeholder="项目名称1-50个字符"/>
        </FormItem>
        <FormItem label="项目Key" prop="PBKey">
          <Input v-model="formItem.PBKey" placeholder="项目唯一标示，1-10英文字符"/>
        </FormItem>
        <FormItem label="平台" prop="PBPlatform">
          <Select v-model="formItem.PBPlatform" :filterable="true" placeholder="项目平台">
            <Option v-for="platform in platforms" :key="platform.id" :value="platform.DicDataValue">{{ platform.DicDataName }}</Option>
          </Select>
        </FormItem>
        <FormItem label="负责人" prop="PBLead">
          <Select v-model="formItem.PBLead" :filterable="true" placeholder="项目负责人">
            <Option v-for="user in userList" :key="user.id" :value="user.id">{{ user.last_name }}{{ user.first_name }} ({{ user.email }})</Option>
          </Select>
        </FormItem>
        <FormItem label="产品线" prop="Product">
          <Select v-model="formItem.Product" :filterable="true" placeholder="任务类型">
            <Option v-for="product in products" :key="product.id" :value="product.id">{{ product.PTitle }}</Option>
          </Select>
        </FormItem>
        <FormItem label="可见性" prop="PBVisiableLevel">
          <Row>
            <Col span="8" offset="0">
            <RadioGroup v-model="formItem.PBVisiableLevel" vertical>
              <Radio :label="1">
                <Icon type="locked" :size="20" ></Icon>
                <span>私有</span>
                <span style="color:#737373;padding-left: 20px;">项目仅自己可见</span>
              </Radio>
              <Radio :label="2">
                <Icon type="contrast" :size="20"></Icon>
                <span>内部</span>
                <span style="color:#737373;padding-left: 20px;">项目可以被同组成员看到</span>
              </Radio>
              <Radio :label="3">
                <Icon type="ios-world" :size="20"></Icon>
                <span>公开</span>
                <span style="color:#737373;padding-left: 20px;"  >项目对所有人员可见</span>
              </Radio>
            </RadioGroup>
            </Col>
          </Row>
        </FormItem>
      </Form>
    </div>
    <div slot="footer">
      <Button v-if="projectCreateDialogShow" type="success"  style="width: 80px; height:30px;" shape="circle" @click="addProject('projectCreate')">添加</Button>
      <!--<Button type="ghost"  style="width: 80px; height:30px;"  shape="circle" @click="cancel">取消</Button>-->
    </div>
</Modal>
</template>

<script>
import { mapGetters,mapMutations } from 'vuex'
import { projectValidateRules } from './ProjectCreateDialog'
import FormItem from '../../../node_modules/iview/src/components/form/form-item.vue'

  export default {
    name: 'ProjectCreateDialog',
    data () {
      return {
        userList: [],
        platforms: [],
        products: [],
        formItem: {
          PBTitle: '',
          PBKey: '',
          PBLead: 1,
          PBPlatform: 1,
          Product: 1,
          PBVisiableLevel: 1,
          PBCreator: 0
        },
        ruleCustom: {
          ...projectValidateRules
        }
      }

    },
    computed: {
      ...mapGetters('project',['projectCreateDialogShow']),
      ...mapGetters(['appBodyHeight']),
      containerHeight: function () {
        return this.appBodyHeight-100
      },
    },
    methods:
      {
        ...mapMutations('project', ['setProjectCreateDialogShow', 'setProjectAdded']),
        addProject (name) {
          this.$refs[name].validate((valid) => {
            if (valid) {
              this.$axios.post('/api/project/list', this.formItem).then(response => {
                this.setProjectCreateDialogShow(false)
                this.setProjectAdded(true)
              }, response => {
                this.setProjectCreateDialogShow(false)
                this.$Message.error({
                  content: '创建项目失败，请联系管理员或者重试',
                  duration: 10
                })
              })

            }
          })
        },
        cancel () {
          this.setProjectCreateDialogShow(false)
        },
      },
    created () {
      this.$axios.get('/api/common/dicconfig/5/dicconfigs').then(response => {
        this.platforms=response.data.result
      }, response => {
        // error callback
      })

      this.$axios.get('/api/common/users/list').then(response => {
        this.userList=response.data.result
      }, response => {
        // error callback
      })

      this.$axios.get('/api/project/products').then(response => {
        this.products=response.data.result
      }, response => {
        // error callback
      })

    },
    mounted () {

    },
    watch: {

    },
    components: {
      FormItem
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
