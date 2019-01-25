

const apiRouter = [
  {
    name: 'envRoot',
    path: '/interface/mock',
    components: {
      default: function () {
        return import('../pages/interface/mock/APIMockWebpart.vue')
      },
      bodyhead: function () {
        return import('../pages/interface/Head.vue')
      }
    },
    meta: ''
  },
  { path: '/interface', redirect: '/interface/mock' }
]

export {
  apiRouter
}
