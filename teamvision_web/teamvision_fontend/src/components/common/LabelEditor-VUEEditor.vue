<template>
  <div>
    <Tooltip content="点击开始编辑" transfer="">
      <div v-if="show" @mouseout="onMouseOut" class="cursor-hand" @click="onClickEdit" @mouseover="onMouseOver">
        <span style="" v-html="displayValue">{{ displayValue }}</span>
        <span v-if="mouseHover" style="margin-top:-10px;">
        <Icon type="ios-create-outline" :size="18" class="cursor-hand"/>
      </span>
      </div>
    </Tooltip>
    <vue-editor v-if="edited"  v-model="editValue" :editorToolbar="editorToolBar"  :placeholder="placeHolder">
    </vue-editor>
    <ButtonGroup v-if="edited" slot="suffix" style="width: 100px; margin-left: 0px; padding-top: 13px;" shape="circle" size="small">
      <Button type="primary" @click="onOk" ghost>保存</Button>
      <Button @click="onCancel">取消</Button>
    </ButtonGroup>
  </div>
</template>

<script>

import { VueEditor } from 'vue2-editor'
export default {
  name: 'labelEditorVueEditor',
  props: ['placeHolder', 'displayText'],
  data () {
    return {
      editorToolBar: [
        ['bold', 'italic', 'underline'],
        [{'list': 'ordered'}, {'list': 'bullet'}],[{ 'color': [] }, { 'background': [] }],
      ],
      editValue: '',
      displayValue: '',
      mouseHover: false,
      edited: false,
      show: true
    }
  },
  computed: {
  },
  methods: {
    onMouseOver: function () {
      this.mouseHover = true
    },

    onMouseOut: function () {
      this.mouseHover = false
    },

    onClickEdit: function () {
      this.mouseHover = false
      this.show = false
      this.edited = true
    },
    onCancel: function () {
      this.mouseHover = false
      this.show = true
      this.edited = false
    },
    onOk: function () {
      this.displayValue = this.editValue
      this.$emit('updateValue', this.editValue)
      this.mouseHover = false
      this.show = true
      this.edited = false
    }

  },
  created: function () {
    this.displayValue = this.displayText
    this.editValue = this.displayText
  },
  watch: {
    displayText: function () {
      this.displayValue = this.displayText
      this.editValue = this.displayText
      this.show = true
      this.mouseHover = false
    }
  },
  components: {
    VueEditor
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
