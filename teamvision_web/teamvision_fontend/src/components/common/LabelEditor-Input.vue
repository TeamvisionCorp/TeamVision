<template>
  <div>
    <!--<div v-if="mouseHover" @mouseout="onMouseOut" style="height: 35px; border: 1px solid #f5f7f9;border-radius: 5px;">-->
      <!--<span style="padding:10px;">{{ displayValue }}</span>-->
      <!--<span @click="onClickEdit" class="pull-left" style="margin-top:-10px;">-->
        <!--<Icon type="ios-create-outline" :size="18" class="cursor-hand"/>-->
      <!--</span>-->
    <!--</div>-->
    <div v-if="readonly"  @mouseover="onMouseOver" @mouseout="onMouseOut">
      <Poptip trigger="hover"  :content="displayValue">
        <span :style="'width:' + displayWidth +'px'" class="text-display">
          <span style="width: 20px;height: 18px;"><Icon v-if="mouseHover"  @click="onClickEdit"  type="ios-create-outline" :size="18" class="cursor-hand"/></span>
          {{ displayValue }}
        </span>
      </Poptip>
    </div>
    <Input v-if="edited" v-model="editValue" :placeholder="placeHolder">
    <ButtonGroup slot="suffix" style="width: 100px; margin-left: 10px; padding-top: 0px;" shape="circle" size="small">
      <Icon :size="20" @click="onOk(id)" color="black" class="cursor-hand" type="md-checkmark" />
      <Icon :size="20" @click="onCancel(id)" color="black" class="cursor-hand" type="md-close" />
    </ButtonGroup>
    </Input>
  </div>
</template>

<script>
  export default {
    name: 'labelEditorInput',
    props: ['placeHolder', 'displayText','editing','displayWidth','id'],
    data () {
      return {
        editValue: '',
        displayValue: '',
        mouseHover: false,
        edited: false,
        readonly: true
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

      onClickEdit: function (e) {
        this.mouseHover = false
        this.readonly = false
        this.edited = true
      },
      onCancel: function (id) {
        this.mouseHover = false
        this.readonly = true
        this.edited = false
        this.$emit('cancelUpdate', this.editValue,id)
      },
      onOk: function (id) {
        this.displayValue = this.editValue
        this.$emit('updateValue', this.editValue,id)
        this.mouseHover = false
        this.readonly = true
        this.edited = false
      },

      initInputDisplayState: function () {
        if (this.editing) {
          this.readonly = false
          this.edited = true
        }
      }

    },
    created: function () {
      this.displayValue = this.displayText
      this.editValue = this.displayText
      this.initInputDisplayState()
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
.text-display {
  display: inline-flex;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  padding: 10px;

}

</style>
