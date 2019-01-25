import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  projectCreateDialogShow: false,
  projectSearchKey: '',
  projectAdded: false
}
const getters = {

  projectCreateDialogShow (state) {
    return state.projectCreateDialogShow
  },

  projectSearchKey (state) {
    return state.projectSearchKey
  },
  projectAdded (state) {
    return state.projectAdded
  }
}
const mutations = {
  setProjectCreateDialogShow (state, isShow) {
    state.projectCreateDialogShow = isShow
  },

  setProjectSearchKey (state, key) {
    state.projectSearchKey = key
  },

  setProjectAdded (state,key) {
    state.projectAdded = key
  }
}
const actions = {

  setProjectCreateDialogShowAction (context, isShow) {
    context.commit('setProjectSearchKey', isShow)
  },

  setProjectSearchKeyAction (context, key) {
    context.commit('setProjectSearchKey', key)
  },
  setProjectAddedAction (context, key) {
    context.commit('setProjectAdded', key)
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
