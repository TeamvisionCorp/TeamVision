import Vue from 'vue'
import Vuex from 'vuex'
import task from './project/task'
import issue from './project/issue'
import fortesting from './project/fortesting'
import project from './project/project'
import projectglobal from './project/projectglobal'
import citask from './ci/citask'
import citaskflow from './ci/citaskflow'
import mockapi from './interface/mockapi'

Vue.use(Vuex)

const state = {
  appBodyHeight: 0,
  inProject: false,
  userInfo: {}
}
const getters = {
  appBodyHeight (state) {
    return state.appBodyHeight
  },
  inProject (state) {
    return state.inProject
  },

  userInfo (state) {
    return state.userInfo
  }

}
const mutations = {
  setAppBodyHeight (state, height) {
    state.appBodyHeight = height
  },
  setInProject (state, inProject) {
    state.inProject = inProject
  },
  setUserInfo (state, userInfo) {
    state.userInfo = userInfo
  }
}
const actions = {
  setAppBodyHeight (context, height) {
    context.commit('setAppBodyHeight', height)
  },

  setInProjectAction (context, height) {
    context.commit('setInProject', height)
  }
}
const modules = {
  task,
  citask,
  project,
  citaskflow,
  mockapi,
  fortesting,
  projectglobal,
  issue
}

const store = new Vuex.Store({
  strict: true,
  actions,
  getters,
  modules,
  state,
  mutations
})

export default store
