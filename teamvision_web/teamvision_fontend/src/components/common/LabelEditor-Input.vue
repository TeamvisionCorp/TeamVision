<template>
  <div>
    <!--<div v-if="mouseHover" @mouseout="onMouseOut" style="height: 35px; border: 1px solid #f5f7f9;border-radius: 5px;">-->
      <!--<span style="padding:10px;">{{ displayValue }}</span>-->
      <!--<span @click="onClickEdit" class="pull-left" style="margin-top:-10px;">-->
        <!--<Icon type="ios-create-outline" :size="18" class="cursor-hand"/>-->
      <!--</span>-->
    <!--</div>-->
    <div v-if="show"  @mouseover="onMouseOver" @mouseout="onMouseOut">
      <span style="padding:10px;">{{ displayValue }}</span>
      <span v-if="mouseHover"  @click="onClickEdit" class="pull-left" style="margin-top:-10px;">
        <Icon type="ios-create-outline" :size="18" class="cursor-hand"/>
      </span>
    </div>
    <Input v-if="edited" v-model="editValue" :placeholder="placeHolder">
    <ButtonGroup slot="suffix" style="width: 100px; margin-left: 40px; padding-top: 3px;" shape="circle" size="small">
      <Button type="primary" @click="onOk" ghost>保存</Button>
      <Button @click="onCancel">取消</Button>
    </ButtonGroup>
    </Input>
  </div>
</template>

<script>
  export default {
    name: 'labelEditorInput',
    props: ['placeHolder', 'displayText'],
    data () {
      return {
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
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
