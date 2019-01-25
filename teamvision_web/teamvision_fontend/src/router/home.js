
const homeRouter = [
  {
    name: 'homeRoot',
    path: '/home/summary',
    components: {
      default: function () {
        return import('../pages/home/HomeSummary.vue')
      },
      bodyhead: function () {
        return import('../pages/home/Head.vue')
      }
    },
    meta: ''
  },
  {
    name: 'homeTask',
    path: '/home/my/task',
    components: {
      default: function () {
        return import('../pages/project/projecttask/ProjectTask.vue')
      },
      bodyhead: function () {
        return import('../pages/home/Head.vue')
      }
    },
    props: {bodyhead: true, default: true},
    meta: ''
  },

  {
    name: 'homeFortesting',
    path: '/home/my/fortesting',
    components: {
      default: function () {
        return import('../pages/project/project-fortesting/ProjectFortesting.vue')
      },
      bodyhead: function () {
        return import('../pages/home/Head.vue')
      }
    },
    props: {bodyhead: true, default: true},
    meta: ''
  },

  {
    name: 'homeIssue',
    path: '/home/my/issue',
    components: {
      default: function () {
        return import('../pages/project/issue/ProjectIssue.vue')
      },
      bodyhead: function () {
        return import('../pages/home/Head.vue')
      }
    },
    props: {default: true,bodyhead: true},
    meta: ''
  },

  { path: '/', redirect: '/home/summary' },
  { path: '/home', redirect: '/home/summary' },
  { path: '/home/task/all', redirect: '/home/my/task' },
  { path: '/home/task/', redirect: '/home/my/task' }
]

export {
  homeRouter
}
