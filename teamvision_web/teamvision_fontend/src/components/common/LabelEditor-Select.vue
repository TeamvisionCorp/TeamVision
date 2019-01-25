<template>
  <div>
    <div v-if="mouseHover" @mouseout="onMouseOut" style="height: 35px; border: 1px solid #f5f7f9;border-radius: 5px;">
      <span style="padding:10px;">{{ displayValue }}</span>
      <span @click="onClickEdit" class="pull-left" style="margin-top:-10px;"><Icon type="ios-create-outline" :size="18"
                                                                                   class="cursor-hand"/></span>
    </div>
    <div v-if="show" @mouseover="onMouseOver">
      <span style="padding:10px;">{{ displayValue }}</span>
    </div>
    <div v-if="edited">
      <Select v-model="editValue" filterable :label-in-value="true" @on-change="onSelectValueChange">
        <Option v-for="item in optionList" :value="item.id" :key="item.id">{{ item.label }}</Option>
      </Select>
      <ButtonGroup style="margin-left:10px;" shape="circle" size="small">
        <Button type="primary" @click="onOk" ghost>保存</Button>
        <Button @click="onCancel">取消</Button>
      </ButtonGroup>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'labelEditorSelect',
    props: ['optionList', 'displayText','value'],
    data () {
      return {
        editValue: '',
        displayValue: '',
        editText: '',
        mouseHover: false,
        edited: false,
        show: true
      }
    },
    methods: {
      onMouseOver: function () {
        this.mouseHover = true
        this.show = false
      },

      onMouseOut: function () {
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
        this.displayValue = this.editText
        this.$emit('updateValue', this.editValue)
        this.mouseHover = false
        this.show = true
        this.edited = false
      },

      onSelectValueChange: function (value) {
        console.log(value)
        this.editValue = value.value
        this.editText = value.label
      }



    },
    created: function () {
      this.editValue = this.value
      this.displayValue = this.displayText
      this.editText = this.displayText
    },
    watch: {
      displayText: function () {
        this.displayValue = this.displayText
        this.editText = this.displayText
      },
      value: function () {
        this.editValue = this.value
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">

</style>
