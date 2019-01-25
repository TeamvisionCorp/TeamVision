<template>
  <div  style="">
    <Modal :value="true" :closable="false" fullscreen title="上传附件" footer-hide>
          <Upload ref="upload" multiple type="drag" paste action="/api/project/issue/attachments"
                  :on-success="handleSuccess"
                  :on-remove="handleRemove"
                  :format="[]"
                  :max-size="10240"
                  :default-file-list="defaultList"
                  :on-format-error="handleFormatError"
                  :on-exceeded-size="handleMaxSize">
            <div style="padding: 20px 0">
              <Icon type="ios-cloud-upload" size="52" style="color: #3399ff"></Icon>
              <p>点击，拖拽，粘贴上传附件</p>
            </div>
          </Upload>
      <div style="padding-top: 20px; float: right;">
        <Button @click="onPatchIssueAttachment" type="primary" size="default" shape="circle">确认上传</Button>
      </div>
    </Modal>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import { mapGetters, mapMutations } from 'vuex'
import projectIssueFilter from './ProjectIssueFilter.vue'
import projectIssueList from './ProjectIssueList.vue'
import ProjectIssueCreateDialog from './ProjectIssueCreateDialog.vue'
import ProjectIssueItem from './ProjectIssueItem.vue'
import ProjectIssueDetail from './ProjectIssueDetail.vue'
import { axiosSync } from './ProjectIssue'

export default {
  name: 'IssueAttachmentsMobileUpload',
  props: {
    issueID: {
      type: [Number,String],
      default: 0
    }
  },
  data () {
    return {
      uploadList: [],
      defaultList: [],
    }
  },
  computed: {
    ...mapGetters(['appBodyHeight'])
  },
  methods:
      {
        ...mapMutations('issue', ['setIssueChange', 'setShowIssueDetail','setSelectIssueID']),
        ...mapMutations('projectglobal', ['setViewDialogShow','setProject']),

        handleSuccess (res, file, fileList) {
          file.url = res.result.url
          file.id = res.result.file_id
          this.uploadList.push(file.id)
        },

        handleRemove (file, fileList) {
          this.uploadList = fileList
        },

        handleFormatError (file) {
          this.$Message.warning({
            content: '文件格式不正确,格式：\'jpg\',\'jpeg\',\'png\'',
            duration: 10,
            closable: true
          })
        },
        handleMaxSize (file) {
          this.$Message.warning({
            content: '文件大小超过10M限制',
            duration: 10,
            closable: true
          })
        },
        onPatchIssueAttachment: function () {
          let paras = {}
          paras['uploadList'] = this.uploadList
          this.$axios.patch('/api/project/issue/' + this.issueID + '/attachment/0',paras).then(response => {
            this.$Message.success({
              content: '文件上传成功',
              duration: 10,
              closable: true
            })
            this.$refs['upload'].clearFiles()
            this.uploadList = []
          }, response => {
            this.uploadList = []
          })
        }
      },
  created: function () {
  },
  mounted: function () {
  },
  watch: {
  },

  components: {
    draggable,
    projectIssueFilter,
    ProjectIssueCreateDialog,
    ProjectIssueItem,
    projectIssueList,
    ProjectIssueDetail
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .board-column-item {
    margin-bottom: 5px;
    margin-top: 5px;
    min-height: 74px;
    max-height: 200px;
    width: 280px;
  }

  .board-item-priority {
    width: 1px;
    display: inline-block;
    float: left;
    height:170px;
  }

  .board-item-body {
    width: 235px;
    display: inline-table;
    word-wrap: break-word;
    white-space: initial;
    padding: 10px;

  }

  .board-item-rightbar {
    display: inline-table;
  }

  .board-item-avatar {
    margin-right: 15px;
    margin-top: 10px;
  }

  .ivu-drawer-body {
    width: 100%;
    height: calc(100% - 51px);
    padding: 0px !important;
    font-size: 12px;
    line-height: 1.5;
    word-wrap: break-word;
    position: absolute;
    overflow: auto;
  }

</style>
