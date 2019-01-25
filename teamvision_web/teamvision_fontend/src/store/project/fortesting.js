import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  createDialogShow: false,
  viewDialogShow: false,
  projectVersion: 0,
  project: 0,
  taskChange: false
}
const getters = {
  createDialogShow (state) {
    return state.createDialogShow
  },
  viewDialogShow (state) {
    return state.viewDialogShow
  },
  projectVersion (state) {
    return state.projectVersion
  },
  taskChange (state) {
    return state.taskChange
  }

}
const mutations = {
  setCreateDialogShow (state, isShow) {
    state.createDialogShow = isShow
  },
  setViewDialogShow (state, isShow) {
    state.viewDialogShow = isShow
  },
  setProjectVersion (state, versionID) {
    state.projectVersion = versionID
  },

  setTaskChange (state, isChange) {
    state.taskChange = isChange
  },
}
const actions = {
  setCreateDialogShowAction (context, isShow) {
    context.commit('setCreateDialogShow', isShow)
  },
  setViewDialogShowAction (context, isShow) {
    context.commit('setViewDialogShow', isShow)
  },
  setProjectVersionAction (context, versionID) {
    context.commit('setProjectVersion', versionID)
  },
  setTaskChangeAction (context, isChanged) {
    context.commit('setTaskChange', isChanged)
  }
}
const modules = {}

export default {
  namespaced: true,
  actions,
  getters,
  state,
  mutations,
  modules
}
