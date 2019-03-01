<template>
  <div>
    <Card dis-hover :padding="10" style="color: #f5f5f5">
      <Breadcrumb>
        <BreadcrumbItem to="/">Home</BreadcrumbItem>
        <BreadcrumbItem to="/components/breadcrumb">Components</BreadcrumbItem>
        <BreadcrumbItem>Breadcrumb</BreadcrumbItem>
      </Breadcrumb>
    </Card>
    <div :style="'padding:16px;overflow-y:auto;height:'+ containerHeight+'px'" >
      <Card v-if="document.Type === 1" :key="document.id" v-for="document in projectFiles" dis-hover :padding="0" class="document-card">
        <div style="padding-left: 10px;padding-right: 10px;">
          <span><Icon :size="16" type="ios-folder"></Icon></span>
          <span class="pull-right">
            <span>
              <Dropdown @on-click="openDialog">
        <a href="javascript:void(0)">
            <Icon type="ios-list" />
        </a>
        <DropdownMenu slot="list" style="margin-left: -20px;">
          <DropdownItem :name="'1:' + document.id" style="padding: 0px;   padding-left: 16px;"><Icon :size="16" type="ios-trash"></Icon> 删除</DropdownItem>
          <DropdownItem :name="'2:' + document.id"  style="padding: 0px;   padding-left: 16px;"><Icon :size="16" type="ios-trash"></Icon> 移动</DropdownItem>
        </DropdownMenu>
    </Dropdown>
            </span>
          </span>
        </div>
        <Divider style="margin-top: 5px;margin-bottom:5px;"/>
          <div style="padding-left: 10px;padding-right: 10px;">
            <center style="display: block;height:80px;padding-top: 20px;">
              <label-editor-input :id="document.id" :editing="document.id === 0" :displayWidth="140" @updateValue="updateDocumentTitle" placeHolder="问题标题"  :displayText="document.FileName"></label-editor-input>
            </center>
          </div>
        <div>
          <center>
            <router-link :to="'/project/' + projectID + '/documents/' + document.id"  :exact="false" tag="span"  class="cursor-hand">
              <a style="width: 40px;display: inline-block;text-decoration: underline;color:inherit;" class="cursor-hand">打开</a>
            </router-link>
          </center>
        </div>
      </Card>
      <Card v-if="document.Type === 2" v-for="document in projectFiles" :key="document.id" dis-hover :padding="0" class="document-card">
        <div style="padding-left: 10px;padding-right: 10px;">
          <span style="padding-top: 5px;">
            <i class="fa fa-file-excel-o fa-fw"></i>
          </span>
          <span class="pull-right">
            <span>
              <Dropdown @on-click="openDialog">
        <a href="javascript:void(0)">
            <Icon type="ios-list" />
        </a>
        <DropdownMenu slot="list" style="margin-left: -20px;">
            <DropdownItem :name="'1:' + document.id" style="padding: 0px; padding-left: 16px;"><Icon :size="16" type="ios-trash"></Icon> 删除</DropdownItem>
            <DropdownItem :name="'2:' + document.id" style="padding: 0px;   padding-left: 16px;"><Icon :size="16" type="ios-trash"></Icon> 移动</DropdownItem>
        </DropdownMenu>
    </Dropdown>
              </span>
          </span>
        </div>
        <Divider style="margin-top: 5px;margin-bottom:5px;"/>
        <div style="padding-left: 10px;padding-right: 10px;">
          <center style="display: block;height:80px;padding-top: 20px;">
            <label-editor-input :id="document.id" :editing="document.id === 0" @updateValue="updateDocumentTitle" :displayWidth="140" placeHolder="问题标题"  :displayText="document.FileName"></label-editor-input>
          </center>
        </div>
        <div>
          <center>
            <router-link :to="'/project/documents/excel/' + document.id"  :exact="false" tag="span"  class="cursor-hand">
              <a style="width: 40px;display: inline-block;text-decoration: underline;color: inherit;" target="_blank" class="cursor-hand">查看</a>
            </router-link>
            <router-link :to="'/project/documents/excel/' + document.id" :exact="false" tag="span"  class="cursor-hand">
              <a style="width: 60px;display: inline-block;text-decoration: underline;color: inherit" target="_blank" class="cursor-hand">编辑</a>
            </router-link>
          </center>
        </div>
      </Card>
    </div>
    <kendo-dialog ref="dialog" :modal="true" :height="400"
                  :width="600"
                  :visible="false"
                  :title="'文件夹'"
                  :closable="false">
      <kendo-tree-view ref="treeview" :data-source="remoteDataSource"
                      :data-text-field="'FileName'"
                       @select="onSelectFolder">
      </kendo-tree-view>
      <kendo-dialog-action :text="'取消'" :action="cancelMove"></kendo-dialog-action>
      <kendo-dialog-action :text="'移动'" :action="moveDocument"
                           :primary="true">
      </kendo-dialog-action>
    </kendo-dialog>

    <kendo-dialog ref="deleteConfirmDialog" :modal="true"
                  :width="280"
                  :visible="false"
                  :title="'删除确认'">
      <div>点击确定，删除文件！</div>
      <kendo-dialog-action :text="'取消'" :action="cancelMove"></kendo-dialog-action>
      <kendo-dialog-action :text="'删除'"
                           :primary="true"
                           :action="deleteDocument">
      </kendo-dialog-action>
    </kendo-dialog>
  </div>
</template>

<script>
  import { mapGetters, mapMutations } from 'vuex'
  import labelEditorInput from '../../../components/common/LabelEditor-Input.vue'
  import { KendoDialog, KendoDialogAction } from '@progress/kendo-dialog-vue-wrapper'
  import { KendoTreeView } from '@progress/kendo-treeview-vue-wrapper'


  export default {
    name: 'ProjectDocuments',
    props: ['projectID','folderID'],
    data () {
      return {
        projectFiles: [],
        selectedFolder: 0,
        selectedDocument: 0,
        formData: {
          id: 0,
          ProjectID: 0,
          Type: 1,
          FileID: 0,
          Owner: 0,
          FileName: '',
          Parent: null
        }
      }
    },
    computed: {
      ...mapGetters(['appBodyHeight']),
      ...mapGetters('projectglobal',['createDocumentType']),
      containerHeight: function () {
        return this.appBodyHeight
      },

      folder: function () {
        if (this.folderID) {
          return this.folderID
        } else {
          return ''
        }
      },

      remoteDataSource: function () {
        return new kendo.data.HierarchicalDataSource({
          transport: {
            read: {
              url: '/api/project/' + this.projectID + '/documents/?Parent__isnull=True&ReadOnly=False&Type=1',
              dataType: 'json'
            }
          },
          schema: {
            model: {
              id: 'id',
              hasChildren: 'HasChild'
            },
            data: function (resp) {
              let root = {
                id: null,
                ProjectID: 0,
                Type: 1,
                FileID: 0,
                Owner: 0,
                FileName: '根目录',
                Parent: null
              }
              let soucreData = resp.result
               soucreData.splice(0,0,root)
              return soucreData
            }
          }
        })
      }
    },

    methods: {
      ...mapMutations('projectglobal',['setCreateDocumentType']),
      updateDocumentTitle: function (title,id) {
        if (parseInt(id)=== 0){
          if (title!=='') {
            this.formData.FileName = title
            this.$axios.post('/api/project/' + this.projectID + '/documents/',this.formData).then(response => {
//              let tempData = response.data.result
              this.loadProjectDocuments(this.projectID,this.folder)
            }, response => {
              // error callback
            })
          }
        } else {
          this.$axios.patch('/api/project/document/'+ id +'/',{FileName: title}).then(response => {
//            let tempData = response.data.result
            console.log(tempData)
          }, response => {
            // error callback
          })
        }
        this.setCreateDocumentType(0)
      },

      addFolder: function (value) {
        if (value === 1)
        {
          let folder = this.formData
          folder.FileName = '新建文件夹'
          folder.Type = value
          folder.ProjectID = this.projectID
          this.projectFiles.push(folder)
        }

        if (value === 2)
        {
          let folder = this.formData
          folder.Type = value
          folder.FileName = '新建Excel.xlsx'
          folder.ProjectID = this.projectID
          this.projectFiles.push(folder)
        }
      },

      openDialog: function (documentID) {
        let actions = documentID.split(':')
        this.selectedDocument = parseInt(actions[1])
        if (parseInt(actions[0]) === 2 ) {
          this.$refs.dialog.kendoWidget().open()
        }

        if (parseInt(actions[0]) === 1 ) {
          this.$refs.deleteConfirmDialog.kendoWidget().open()
        }
      },

      deleteDocument: function () {
        if (this.selectedDocument !== 0) {
          this.$axios.delete('/api/project/document/' + this.selectedDocument).then(response => {
            this.removeDocumentFromFolder(this.selectedDocument)
            this.selectedDocument = 0
          }, response => {
            // error callback
          })
        }
      },

      moveDocument: function (e) {
        if (this.selectedDocument !==0 && this.selectedFolder !==0) {
          this.$axios.patch('/api/project/document/' + this.selectedDocument + '/', {Parent: this.selectedFolder}).then(response => {
            this.removeDocumentFromFolder(this.selectedDocument)
            this.selectedDocument = 0
            this.selectedFolder = 0
          }, response => {
            // error callback
          })
        }
      },

      cancelMove: function () {
        this.selectedDocument = 0
        this.selectedFolder = 0
      },

      onSelectFolder: function (e) {
        let item = this.$refs.treeview.kendoWidget().dataItem(e.node)
        this.selectedFolder = item.id
      },

      removeDocumentFromFolder: function (documentID) {
        for(let i=0;i<this.projectFiles.length;i++){
          if (this.projectFiles[i].id === parseInt(documentID)) {
            this.projectFiles.splice(i,1)
          }
        }

      },

      loadProjectDocuments: function (projectID,folderID) {
        let documentFilter = '?Parent__isnull=True'
        if (folderID) {
          documentFilter = '?Parent=' + folderID
        }
        this.$axios.get('/api/project/' + projectID + '/documents' + documentFilter).then(response => {
          let tempData = response.data.result
          this.projectFiles = tempData
        }, response => {
          // error callback
        })
      }
    },

    created: function() {
      console.log(this.projectID)
      console.log(this.folder)
      this.loadProjectDocuments(this.projectID,this.folder)
    },

    watch: {

      createDocumentType: function (value) {
        if (value !== 0) {
          this.addFolder(value)
        }
      },

      folder: function () {
        this.loadProjectDocuments(this.projectID,this.folder)
      }
    },

    components: {
      labelEditorInput,
      KendoDialog,
      KendoDialogAction,
      KendoTreeView
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

.document-card {
  width: 200px;
  height: 150px;
  margin:10px;
  float:left;
}

</style>
