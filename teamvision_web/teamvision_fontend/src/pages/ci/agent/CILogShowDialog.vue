<template>
  <Modal :value="dialogShow" title="日志信息"  @on-visible-change="showLogInfo"  @on-cancel="cancel" :styles="{bottom:'20px',top: '50px',width: '80%', 'margin-left': 'auto','margin-right': 'auto'}">
    <div slot="header" style="text-align:left">
      <span>任务ID为 [{{ taskID }}] 的任务日志</span>
      <Checkbox v-model="scrollToBottom" class="pull-right" style="margin-right: 100px;">默认滚动到底部</Checkbox>
    </div>
    <div id="ciLogContainer" style="height: 600px;overflow-y: scroll;overflow-x: hidden;color:rgb(0, 255, 0);background-color: black;padding:20px;word-break: break-all">
      <div>
        <div v-if="preLogLink"><a @click="onViewOldLog">查看之前的日志</a></div>
        <div v-html="preLog">{{ preLog }}</div>
      </div>
      <div v-html="log" >{{ log }}</div>
    </div>
    <div slot="footer">
    </div>
</Modal>
</template>

<script>
import { mapGetters, mapMutations} from 'vuex'

  export default {
    name: 'CILogShowDialog',
    props: ['taskID','tqID','taskUUID'],
    components: {
    },
    data () {
      return {
        log: '',
        preLog: '',
        preLogLink: true,
        scrollToBottom: true
      }

    },
    computed: {
      ...mapGetters('citask', ['ciLogDialogShow']),
      dialogShow: function () {
        return this.ciLogDialogShow
      },
      loginfo: function () {
        return this.log
      }

    },
    methods:
      {
        ...mapMutations('citask', ['setCILogDialogShow']),
        cancel: function () {
          this.setCILogDialogShow(false)
          this.preLog = ''
          this.preLogLink = true
        },
        showLogInfo: function (value) {
          let ws = new WebSocket('ws://'+window.location.host+'/ws/' + this.tqID + '?subscribe-broadcast&publish-broadcast&echo')
          if(value)
          {
            ws.onopen = () => {
              console.log("websocket connected")
            }
            ws.onmessage = evt =>  {
              if(evt.data!=='--heartbeat--')
              {
                this.log = this.log + evt.data + '</br>'
                if(this.scrollToBottom)
                {
                  let logConatiner = document.getElementById('ciLogContainer')
                  logConatiner.scrollTop= logConatiner.scrollHeight
                }

              }
            }

            ws.onerror = evt =>  {
              console.error(evt)
            }
            ws.onclose = evt => {
              console.log("connection closed")
            }
          }
          else
          {
            ws.close()
            this.log = ''
          }

        },

        onViewOldLog: function () {
          this.$axios.get('/api/ci/task/prelog/' + this.tqID).then(response => {
            this.preLog = response.data.result.PreLog
            this.preLogLink = false
          }, response => {

          })
        }
      },
    created () {

    },
    mounted () {

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
  .demo-upload-list{
    display: inline-block;
    width: 60px;
    height: 60px;
    text-align: center;
    line-height: 60px;
    border: 1px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    background: #fff;
    position: relative;
    box-shadow: 0 1px 1px rgba(0,0,0,.2);
    margin-right: 4px;
  }
  .demo-upload-list img{
    width: 100%;
    height: 100%;
  }
  .demo-upload-list-cover{
    display: none;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0,0,0,.6);
  }
  .demo-upload-list:hover .demo-upload-list-cover{
    display: block;
  }
  .demo-upload-list-cover i{
    color: #fff;
    font-size: 20px;
    cursor: pointer;
    margin: 0 2px;
  }
</style>
