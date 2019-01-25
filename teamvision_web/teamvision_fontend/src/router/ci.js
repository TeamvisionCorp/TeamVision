
const ciRouter = [
  {
    name: 'ciRoot',
    path: '/ci',
    redirect: '/ci/task',
    meta: ''
  },
  {
    name: 'ciTaskFlow',
    path: '/ci/:menuItem',
    components: {
      default: function () {
        return import('../pages/ci/CI.vue')
      },
      bodyhead: function () {
        return import('../pages/ci/Head.vue')
      }
    },
    props: {bodyhead: true, default: true},
    meta: ''
  },
  {
    name: 'ciTaskFlowItem',
    path: '/ci/taskflow/:flowID',
    components: {
      default: function () {
        return import('../pages/ci/citaskflow/ci_task_flow_item/CITaskFlowItem.vue')
      },
      bodyhead: function () {
        return import('../pages/ci/citaskflow/ci_task_flow_item/Head.vue')
      }
    },
    props: {bodyhead: true, default: true},
    meta: ''
  },

  {
    name: 'ciTaskFlowHistory',
    path: '/ci/taskflow/:flowID/history',
    components: {
      default: function () {
        return import('../pages/ci/citaskflow/ci_task_flow_item/CITaskFlowHistory.vue')
      },
      bodyhead: function () {
        return import('../pages/ci/citaskflow/ci_task_flow_item/Head.vue')
      }
    },
    props: {bodyhead: true, default: true},
    meta: ''
  }
]

export {
  ciRouter
}
