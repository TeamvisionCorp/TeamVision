<template>
  <div>
    <ul class="api-tree">
                <span class="root-title">
                  <span><Icon type="md-arrow-dropdown" :size="18"/><Icon :size="18" type="ios-folder-outline"
                                                                         style="margin-right: 5px;"/>全部接口</span>
                  <span></span>
                </span>
      <li class="project-node" v-for="project in projectList" :key="project.id">
                  <span  :id="project.id" style="display: block;" class="cursor-hand node-title" v-bind:class="{ 'node-hoverd': nodeHovered }"  @click="onNodeTitleClick('1','project')"  @mouseover="onNodeTitleHover('1','project')" @mouseout="onNodeTitleOut('1','project')">
                    <span v-bind:class="{ 'node-selected': isSelected }" class="node-title">
                      <Icon v-if="extend!==true" :size="18" type="md-arrow-dropright" @click="onExtend('1','project')"/>
                      <Icon v-if="extend" :size="18" type="md-arrow-dropdown" @click="onHide('1','project')"/>
                      <Icon :size="18" type="ios-folder-outline" style="margin-right: 5px;"/> DSP
                    </span>
                    <span v-if="showOperationIcon" class="pull-right" style="padding-right: 20px;" @click="onAddModule('id')">
                      <Tooltip content="添加模块" placement="right" :transfer="true">
                        <Icon :size="18" type="ios-add-circle"/>
                      </Tooltip>
                    </span>
                  </span>
        <ul class="module-node" v-if="extend">
          <span :id="2" style="display: block;" class="cursor-hand node-title" v-bind:class="{ 'node-hoverd': nodeHovered }" @click="onNodeTitleClick('2','module')" @mouseover="onNodeTitleHover('2','module')" @mouseout="onNodeTitleOut('2','module')">
            <span v-bind:class="{ 'node-selected': isSelected }" class="node-title">
               <Icon v-if="extend!==true" :size="18" type="md-arrow-dropright" @click="onExtend('2','module')"/>
              <Icon v-if="extend" :size="18" type="md-arrow-dropdown" @click="onHide('2','module')"/>
              Account
             </span>
            <span v-if="showOperationIcon" class="pull-right" style="padding-right: 15px;" @click="onAddApi('2')" >
                   <Tooltip content="添加接口" placement="right" :transfer="true">
                        <Icon :size="18" type="ios-add-circle"/>
                   </Tooltip>
            </span>
          </span>
          <li class="api-node" v-if="extend">
                      <span :id="3" style="display: block" class="cursor-hand node-title" v-bind:class="{ 'node-hoverd': nodeHovered }" @click="onNodeTitleClick('3','api')" @mouseover="onNodeTitleHover('3','api')" @mouseout="onNodeTitleOut('3','api')">
                           <span v-bind:class="{ 'node-selected': isSelected }" class="node-title"><i class="fa fa-file-code-o fa-fw"></i> api-adrtb</span>
                           <span v-if="showOperationIcon"  class="pull-right" style="padding-right: 10px;" @click="onRemoveApi">
                             <Tooltip content="添加接口" placement="right" :transfer="true">
                              <Icon :size="18" type="ios-remove-circle"/>
                             </Tooltip>
                           </span>
                      </span>
          </li>

        </ul>
      </li>

    </ul>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data () {
      return {
        showOperationIcon: false,
        isSelected: false,
        nodeHovered: false,
        extend: false,
        hovered: false,
        selected: false,
        projectList: [
          {
            id:1,
            type: 'project',
            title: 'DSP',
            extend: false,
            hovered: false,
            selected: false,
            modules: [
              {
                id:1,
                type: 'module',
                title: 'account',
                extend: false,
                hovered: false,
                selected: false,
                apis: [
                  {
                    id:1,
                    type: 'module',
                    title: 'account',
                    extend: false
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    methods: {
      onNodeTitleHover: function (id,nodeType) {
        this.showOperationIcon = true
        this.nodeHovered = true
      },

      onNodeTitleOut: function (id,nodeType) {
        this.showOperationIcon = false
        this.nodeHovered = false
      },

      onNodeTitleClick: function (id,nodeType) {
        this.isSelected = true
        this.$emit('onSelected',id,nodeType)
      },

      onExtend: function (id,nodeType) {
         this.extend = true
      },
      onHide: function (id,nodeType) {
        this.extend = false
      },

      onAddModule: function (id) {
        this.$emit('onAddModule',id)
      },

      onAddApi: function (id) {
        this.$emit('onAddApi',id)
      },

      onRemoveApi: function (id) {
        this.$emit('onRemoveApi',id)
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

  .api-tree {
    text-align: left;
    list-style: none;
    padding-top: 10px;
  }

  .root-title {
    height: 30px;
    padding: 5px;
    display: inline-block;
  }

  .project-node {
    padding: 5px;
    padding-left: 30px;
  }

  .module-node {
    padding: 5px;
    padding-left: 15px;
    list-style: none;
    display: block
  }

  .api-node {
    height: 30px;
    padding: 5px;
    padding-left: 30px;
  }

  .node-selected
  {
    /*background-color: #5e5e5e;*/
    color: #8c0776;
    border-radius: 5px;
    /*opacity: 0.7;*/
  }

  .node-title
  {
    padding: 2px 5px 2px 5px;
  }

  .node-hoverd{

    /*border: 1px solid #8c0776;*/
    /*background-color: #5e5e5e;*/
    color: #8c0776;
    /*border-radius: 5px;*/
    /*opacity: 0.7;*/

  }

</style>
